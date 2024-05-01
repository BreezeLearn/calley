from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI

import os

os.environ["OPENAI_API_KEY"] = "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"


@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' times 'y'."""
    return x * y

@tool
def exponentiate(x: float, y: float) -> float:
    """Raise 'x' to the 'y'."""
    return x**y

@tool
def add(x: float, y: float) -> float:
    """Add 'x' and 'y'."""
    return x + y

prompt = ChatPromptTemplate.from_messages([
    ("system", "you're a helpful assistant"), 
    ("human", "{input}"), 
    ("placeholder", "{agent_scratchpad}"),
])

tools = [multiply, exponentiate, add]


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm = ChatVertexAI(
	model="gemini-pro", 
	temperature=0, 
	convert_system_message_to_human=True,
 project='calley-420915'
)

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

res = agent_executor.invoke({"input": "what's 3 plus 5 raised to the 2.743. also what's 17.24 - 918.1241", })
print(res)