from langchain_google_genai import ChatGoogleGenerativeAI
import os

from langchain.agents import Tool, AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_core.messages import HumanMessage, SystemMessage
# from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.agents import AgentExecutor
from langchain import hub
from langchain import LLMMathChain
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
from Agent.tools.calender_tool import CalenderTool, ScheduleEventTool

os.environ["GOOGLE_API_KEY"] = "AIzaSyDqnLVkETKo7wQgPXN56QON3AGEm4qvTTU"

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    
    handle_parsing_errors=True,
    temperature=0.6,
    max_tokens= 200,
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    },
)
# ddg_search = DuckDuckGoSearchAPIWrapper()
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

tools = [
   CalenderTool(),
   
    Tool.from_function(
        func=llm_math_chain.run,
        name="Calculator",
        description="Useful for when you need to answer questions about very simple math. This tool is only for math questions and nothing else. Only input math expressions. Not supporting symbolic math.",
    ),
]
agent_prompt = hub.pull("mikechan/gemini")
agent_prompt.template = '''Your name is “David”. You are world class ai personal assistant computer that created by Mike Chan(A independent AI engineer). You are highly advanced intelligent. you are very helpful and good to provide information and solve users problem. David is a AELM model (Auto Execution Language Model).



“ David” is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, “ David” is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.



“ David” is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, “ David” is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.



Overall, “ David” is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, “ David” is here to assist.



TOOLS:

------



Assistant has access to the following tools:



{tools}



To use a tool, please use the following format:



```

Thought: Do I need to use a tool? Yes

Action: the action to take, should be one of [{tool_names}]

Action Input: the input to the action

Observation: the result of the action

```



When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:



```

Thought: Do I need to use a tool? No

Final Answer: [your response here]

```



Begin!



Previous conversation history:

{chat_history}



New input: {input}

{agent_scratchpad}

'''


prompt = agent_prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)
llm_with_stop = llm.bind(stop=["\nObservation"])
memory = ConversationBufferMemory(memory_key="chat_history")
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_stop
    | ReActSingleInputOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)
res = agent_executor.invoke({"input": "check the events i have on my calender please?j"})["output"]
print(res)