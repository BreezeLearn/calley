from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from Agent.tools.calender_tool import CalenderTool, ScheduleEventTool
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ChatMessageHistory
import pprint
from langchain_google_vertexai import ChatVertexAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_community.vectorstores import FAISS


os.environ["OPENAI_API_KEY"] = "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"
os.environ["TAVILY_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyDqnLVkETKo7wQgPXN56QON3AGEm4qvTTU"
memory = ChatMessageHistory(session_id="test-session")

chunks = []

def invoke_agent(agent_args, input):
    tools = [CalenderTool(), ScheduleEventTool()]
    if agent_args.web_search is True:
        tools.append(TavilySearchResults())

    prompt = hub.pull("hwchase17/openai-tools-agent")
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", agent_args.instruction or "You are a helpful assistant"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

    llm = ChatVertexAI(
	model="gemini-pro", 
	temperature=0, 
	convert_system_message_to_human=True,
 project='calley-420915'
)

    # Construct the OpenAI Tools agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    res = agent_with_chat_history.invoke(
        {"input": input},
        config={"configurable": {"session_id": "<foo>"}},
    )
        
    return res
