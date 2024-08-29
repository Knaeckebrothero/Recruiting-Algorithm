"""
This module contains functions to generate attributes for the tagging pipeline.
"""
import os
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import StructuredTool
from langchain_chroma import Chroma
from langchain_community.tools.tavily_search import TavilySearchResults


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
        if not (
                os.getenv("TAVILY_API_KEY") or
                os.getenv("OPENAI_API_KEY") or
                os.getenv("CHROMA_DB_PATH")):
            load_dotenv(find_dotenv())
            if not (
                    os.getenv("TAVILY_API_KEY") or
                    os.getenv("OPENAI_API_KEY") or
                    os.getenv("CHROMA_DB_PATH")):
                raise ValueError("Please provide the respective environment variables!")

        # Initialize the search engine
        self._search_engine = TavilySearchResults()

        # Initialize the vector database
        self._vector_database = Chroma(
            persist_directory="./chroma",
            embedding_function=OpenAIEmbeddings()
        )

        # Create tools for storing and retrieving data
        store_key_value = StructuredTool.from_function(
            func=self._store_data,
            name="store_data",
            description="Store a key-value pair in the database."
        )
        retrieve_vale_by_key = StructuredTool.from_function(
            func=self._retrieve_data_search_by_key,
            name="retrieve_data",
            description="Retrieve a list of values from the database based on the given key."
        )

        # Initialize the components
        tools = [self._search_engine, store_key_value, retrieve_vale_by_key]
        llm = ChatOpenAI(model=model, temperature=temperature)
        agent = create_tool_calling_agent(llm, tools=tools, prompt=_format_prompt(prompt))

        # Initialize the agent executor
        self._agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    def __str__(self):
        # TODO: Implement a better string representation.
        return f"OpenAI Agent: {self._agent_executor.agent}"

    def _generate(self, text: str) -> str:
        """
        Generates a response to the given text.

        :param text:
        :return: The generated attributes.
        """
        return self._agent_executor.invoke({'input': text})['output']

    def _store_data(self, key: str, value: str) -> str:
        """
        Stores the given key-value pair in the Chroma database.

        :param key: The key to store the value under.
        :param value: The value to store.
        :return: A message indicating the success or failure of the operation.
        """
        try:
            self._vector_database.add_texts([value], metadatas=[{"key": key}])
            return f"Stored '{key}': '{value}' in the database."
        except Exception as e:
            return f"Error storing data: {e}"

    def _retrieve_data_search_by_key(self, key: str) -> str:
        """
        Retrieves data from the Chroma database based on the given key.

        :param key: The key to search for.
        :return: A message indicating the success or failure of the operation.
        """
        result = "Retrieved the following data:\n"
        try:
            search_results = self._vector_database.similarity_search(key, k=1)
            if search_results:
                for r in search_results:
                    result += f"{r.metadata['key']}: {r.text}\n"
            else:
                result = f"No data found for key '{key}'."
        except Exception as e:
            result = f"Error retrieving data: {e}"
        finally:
            return result
