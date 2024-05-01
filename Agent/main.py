from langchain_google_genai import ChatGoogleGenerativeAI
import os

from langchain.agents import Tool, AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor
from langchain import hub
from langchain import LLMMathChain
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
from Agent.tools.calender_tool import CalenderTool, ScheduleEventTool
import uuid


os.environ["GOOGLE_API_KEY"] = "AIzaSyDqnLVkETKo7wQgPXN56QON3AGEm4qvTTU"
os.environ["TAVILY_API_KEY"] = "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"
memory = ChatMessageHistory(session_id="test-session")


def gemini_agent(agent_args, input, session_id):
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        handle_parsing_errors=True,
        temperature=0.6,
        max_tokens=3000,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
    )
   
    tools = [
        CalenderTool(),
ScheduleEventTool()
       
    ]
    if agent_args.web_search is True:
        tools.append(TavilySearchResults())
    
    agent_prompt = hub.pull("mikechan/gemini")
    agent_prompt.template = f'''Role:

AS a large language model you will take the role and identity of being an/a: "{agent_args.instruction}, and you should never depart from this role. NOTE: ask the user for the necessary tool input do not hallucinate it by yourself
'''+'''
    
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
    # memory = ConversationBufferMemory(memory_key="chat_history")
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

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    # res = agent_executor.invoke({"input": input})
    # print(res)
    # return res

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    random_uuid = uuid.uuid4()

    res = agent_with_chat_history.invoke(
        {"input": input},
        config={"configurable": {"session_id": session_id}},
    )

    return res
