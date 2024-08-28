"""
This module contains functions to generate attributes for the tagging pipeline.
"""
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.agents import AgentExecutor


def _format_prompt(system_prompt: str) -> list:
    """
    Formats the system prompt as a list of messages to be used in a LangChain agent.

    :param system_prompt: The system prompt to format.
    :return: The prompt formatted as a list of messages.
    """
    formatted_messages = [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=[], template=system_prompt)
        ),
        MessagesPlaceholder(variable_name='chat_history', optional=True),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=['input'], template='{input}')
        ),
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ]
    return formatted_messages


class OpenAiAgent:
    """
    This class defines an OpenAI agent for generating attributes based on the given qualifications.

    :_search_engine: The search engine to use for generating attributes.
    :_agent: The agent to use for generating attributes
    """
    _search_engine: TavilySearchResults
    _agent: create_tool_calling_agent

    def __init__(self, prompt, model: str = "gpt-4o-mini", temperature: float = 0):
        """
        Initializes the OpenAI agent.
        The constructor requires the tavily api key to be loaded in the environment.

        :param prompt: The prompt to be used for generating attributes.
        :param model: The OpenAI model to use for generating attributes.
        :param temperature: The temperature to use for generating attributes.
        """
        llm = ChatOpenAI(model=model, temperature=temperature)

        self.set_search_engine(TavilySearchResults())
        self.set_agent(llm, _format_prompt(prompt), [])
        self._agent_executor = AgentExecutor(self._agent, tools=[self._search_engine], verbose=True)

    def set_search_engine(self, search_engine: TavilySearchResults):
        self._search_engine = search_engine

    def set_agent(self, llm, prompt_messages, tools):
        self._agent = create_tool_calling_agent(llm, tools, prompt_messages)

