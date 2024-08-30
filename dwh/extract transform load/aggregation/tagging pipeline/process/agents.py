"""
This module contains agents for generating structured tags.
"""
import os
from dotenv import load_dotenv, find_dotenv
from custom_logger import configure_custom_logger
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import StructuredTool
from langchain_chroma import Chroma
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Optional, List
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage


def _format_prompt(system_prompt: str) -> ChatPromptTemplate:
    """
    Formats the system prompt using langchains template.

    :param system_prompt: The system prompt to format.
    :return: The prompt formatted as a list of messages.
    """
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])


def _format_search_results(results: List[Document]) -> str:
    """
    Formats the search results for display.

    :param results: The search results to format.
    :return: The formatted search results.
    """
    formatted_results = ""
    for r in results:
        # Get the similarity score if available
        similarity = r.metadata.get('score', 'N/A')
        # Format the results
        formatted_results += f"Tag: {r.metadata['key']}\nDescription: {r.page_content}\nSimilarity: {similarity}\n\n"
    return formatted_results


class OpenAiAgent:
    """
    This class defines an OpenAI agent for generating attributes based on the given qualifications.

    The class requires the following environment variables to be set:
    - TAVILY_API_KEY: The API key for the Tavily AI search engine.
    - OPENAI_API_KEY: The API key for the OpenAI API.
    - CHROMA_DB_PATH: The path where the persistent Chroma database should be stored.
    """
    _search_engine: TavilySearchResults
    _vector_database: Chroma

    def __init__(self, prompt, model: str = "gpt-4o-mini", temperature: float = 0):
        """
        Initializes the OpenAI agent.
        The constructor requires the tavily api key to be loaded in the environment.

        :param prompt: The prompt to be used for generating attributes.
        :param model: The OpenAI model to use for generating attributes.
        :param temperature: The temperature to use for generating attributes.
        """
        if not (  # Check if the required environment variables are set
                os.getenv("TAVILY_API_KEY") or
                os.getenv("OPENAI_API_KEY") or
                os.getenv("CHROMA_DB_PATH")):
            load_dotenv(find_dotenv())
            if not (  # Load the environment and check again
                    os.getenv("TAVILY_API_KEY") or
                    os.getenv("OPENAI_API_KEY") or
                    os.getenv("CHROMA_DB_PATH")):
                raise ValueError("Please provide the respective environment variables!")

        # Initialize the logger
        self._log = configure_custom_logger(
            module_name="llm_agent",
            logging_directory=os.getenv('LOGGING_DIRECTORY')
        )
        self._log.debug("Environment variables loaded, logger initialized.")

        # Initialize the search engine
        self._search_engine = TavilySearchResults()
        self._log.debug("Tavily search engine initialized.")

        # Initialize the vector database
        self._vector_database = Chroma(
            persist_directory="./chroma",
            embedding_function=OpenAIEmbeddings()
        )
        self._log.debug("Chroma database initialized.")

        # Create tools for storing and retrieving data
        store_data_tool = StructuredTool.from_function(
            func=self._store_data,
            name="store_data",
            description="Store a key-value pair in the database."
        )
        self._log.debug("Store data tool created.")
        retrieve_data_tool = StructuredTool.from_function(
            func=self._retrieve_data,
            name="retrieve_data",
            description="Retrieve data from the database based on either the key or the value or both."
        )
        self._log.debug("Retrieve data tool created.")

        # Initialize the components
        tools = [self._search_engine, store_data_tool, retrieve_data_tool]
        self._log.debug("Tools initialized.")
        llm = ChatOpenAI(model=model, temperature=temperature)
        self._log.debug("LLM initialized.")
        agent = create_tool_calling_agent(llm, tools=tools, prompt=_format_prompt(prompt))
        self._log.debug("Agent initialized.")

        # Initialize the agent executor
        self._agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        self._log.debug("Agent executor initialized.")

        # Log the initialization
        self._log.info("Agent initialized!")

    def __str__(self):
        self._log.debug("Returning string representation of the agent.")
        return (f"OpenAI Agent: "  # TODO: Implement a better string representation.
                f"{self._agent_executor.agent}, "
                f"{self._agent_executor.tools}")

    def _store_data(self, key: str, value: str) -> str:
        """
        Stores the given key-value pair in the Chroma database.

        :param key: The key to store the value under.
        :param value: The value to store.
        :return: A message indicating the success or failure of the operation.
        """
        self._log.info(f"Agent requested to store '{key}': '{value}' in the database.")
        try:
            self._vector_database.add_texts([value], metadatas=[{"key": key}])
            self._log.info(f"Stored '{key}': '{value}' in the database.")
            return f"Stored '{key}': '{value}' in the database."
        except Exception as e:
            self._log.error(f"Error storing data: {e}")
            return f"Error storing data: {e}"

    def _retrieve_data(self, key: Optional[str] = None, value: Optional[str] = None) -> str:
        """
        Retrieves data from the Chroma database based on the given key or value or both.

        :param key: The key to search for.
        If None, the search will be based on the value.
        :param value: The value to search for.
        If None, the search will be based on the key.
        :return: The retrieved data or an error message.
        """
        self._log.info(f"Agent requested to retrieve data for "
                       f"key: '{key[:50] if key else None}', "
                       f"value: '{value[:50] if value else None}' from the database.")

        if key is None and value is None:
            self._log.warning("No key or value provided for tag retrieval.")
            return "Please provide either a tag name (key) or a description (value) to search for."

        result = "Retrieved the following tags:\n"
        try:
            # Combine key and value for search if both are provided
            search_query = f"{key or ''} {value or ''}".strip()
            self._log.debug(f"Combined search query: '{search_query}'")

            # Perform the search
            search_results = self._vector_database.similarity_search(search_query, k=3)
            self._log.debug(f"Found {len(search_results)} entries.")

            if search_results:
                result += _format_search_results(search_results)
                self._log.debug(f"Formatted search results.")
            else:
                result = f"No matching tags found for the given search criteria."
                self._log.debug(f"No matching tags found for the given search criteria.")

            self._log.debug(f"Retrieved tags: {result}")
        except Exception as e:
            self._log.error(f"Error retrieving tags: {e}")
            result = f"Error retrieving tags: {e}"

        return result

    def generate(self, prompt: str, history: list[AIMessage | HumanMessage] = None) -> str:
        """
        Generates a response to the given text.

        :param prompt: The text to generate a response for.
        :param history: The chat history to provide context for the response (optional).
        :return: The generated response.
        """
        if history is None:
            history = []

        self._log.info(f"Input: {prompt[:25]}, history: {len(history)} | Generating...")
        return self._agent_executor.invoke({
            'input': prompt,
            'chat_history': history
        })['output']
