import sqlite3

import utils.constants as constants
from agent.llms import init_chat_model
from agent.prompts.prompt import get_chat_prompt, get_system_message
from agent.tools.create_support_ticket import create_support_ticket
from agent.tools.lookup_documents import lookup_documents
from agent.tools.save_memory import save_memory
from agent.tools.search_google_shopping import search_google_shopping
from agent.tools.sql_tools import (
    check_and_execute_query_tool,
    sql_db_list_tables,
    sql_db_schema,
)
from IPython.display import Image, display
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import create_react_agent, tools_condition
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.types import Command, interrupt
from typing_extensions import Literal, TypedDict
from utils.utils import create_tool_node_with_fallback, get_path

# store, memory, and cache
# store = InMemoryStore()
memory = SqliteSaver(
    sqlite3.connect(get_path("checkpoints.sqlite", "db"), check_same_thread=False)
)
# set_llm_cache(SQLiteCache(database_path="db/eßcommerce_chatbot_cache.db"))

# tools
safe_tools = []
sensitive_tools = [lookup_documents, create_support_ticket]
tools = safe_tools + sensitive_tools
sensitive_tool_names = {t.name for t in sensitive_tools}
tools_map = {
    "lookup_documents": lookup_documents,
    "create_support_ticket": create_support_ticket
}
def prepare_model_inputs(state: AgentState, config: RunnableConfig, store: BaseStore):
    # Retrieve user memories and add them to the system message
    # This function is called **every time** the model is prompted. It converts the state to a prompt
    user_id = config.get("configurable", {}).get("user_id")
    namespace = ("memories", user_id)
    memories = [m.value["data"] for m in store.search(namespace)]
    system_message = get_system_message(use_hub=False)
    return get_chat_prompt(system_message, memories)

def create_assistant_runnable(chat_model):
    # Retrieve user memories and add them to the system message
    # This function is called **every time** the model is prompted. It converts the state to a prompt
    # user_id = config.get("configurable", {}).get("user_id")
    # namespace = ("memories", user_id)
    # memories = [m.value["data"] for m in store.search(namespace)]
    memories = []
    system_message = get_system_message(use_hub=False)
    return get_chat_prompt(system_message, memories) | chat_model.bind_tools(tools=tools)


# Setup graph
# Graph state schema
class State(MessagesState):
    pass

# Node: Assistant
class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        result = self.runnable.invoke(state)
        return {"messages": result}

def route_tools(state: State):
        next_node = tools_condition(state)
        print("next_node: ", next_node)
        # If no tools are invoked, return to the user
        if next_node == END:
            print("Route to END")
            return END

        ai_message = state["messages"][-1]
        # This assumes single tool calls. To handle parallel tool calling, you'd want to
        # use an ANY condition
        first_tool_call = ai_message.tool_calls[0]
        if first_tool_call["name"] in sensitive_tool_names:
            print("Route to sensitive tools")
            return "sensitive_tools"

        print("Route to safe tools")
        return "safe_tools"

def safe_tools_node(state: State):
    return {"messages": [AIMessage(content="Safe tools node")]}

def sensitive_tools_node(state: State):
    return {"messages": [AIMessage(content="Sensitive tools node")]}

def init_graph(
    model_name=constants.CHAT_MODEL,
    temperature=constants.CHAT_MODEL_TEMPERATURE,
    streaming=True,
):
    # assistant runnable
    chat_model = init_chat_model(
        model_name=model_name,
        temperature=temperature,
        streaming=streaming,
        callbacks=([StreamingStdOutCallbackHandler()] if streaming else []),
    )
    assistant_runnable = create_assistant_runnable(chat_model)

    # Build graph
    builder = StateGraph(State)
    builder.add_node("assistant", Assistant(assistant_runnable))
    builder.add_node("safe_tools", create_tool_node_with_fallback(safe_tools))
    builder.add_node("sensitive_tools", create_tool_node_with_fallback(sensitive_tools))

    # builder.add_node("safe_tools", safe_tools_node)
    # builder.add_node("sensitive_tools", sensitive_tools_node)


    # Define edges: these determine how the control flow moves
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant", route_tools, ["safe_tools", "sensitive_tools", END]
    )
    builder.add_edge("safe_tools", "assistant")
    builder.add_edge("sensitive_tools", "assistant")
    graph_agent = builder.compile(
        checkpointer=memory,
        # store=store,
        interrupt_before=["sensitive_tools"],
        debug=True,
    )

    # print(graph_agent.get_graph().draw_mermaid())
    return graph_agent


# Ref:
# https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/
# https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/
# https://blog.langchain.dev/what-is-a-cognitive-architecture/
# ------------------------------------------------------------
# --- GRAPH AGENT - before use prebuilt create_react_agent ---

# from langchain_core.runnables import Runnable, RunnableConfig
# from langchain_openai import ChatOpenAI
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import START, MessagesState, StateGraph
# from langgraph.prebuilt import tools_condition
# from prompts.prompt import get_chat_prompt
# from tools.lookup_documents import lookup_documents
# from tools.search_google_shopping import search_google_shopping
# from tools.sql_tools import sql_tools
# from utils import create_tool_node_with_fallback

# memory = MemorySaver()

# class State(MessagesState):
#     pass

# class Assistant:
#     def __init__(self, runnable: Runnable):
#         self.runnable = runnable

#     def __call__(self, state: State, config: RunnableConfig):
#         result = self.runnable.invoke(state)
#         return {"messages": result}


# llm = ChatOpenAI(model="gpt-4o-mini")
# # tools = [lookup_documents, *sql_tools]
# tools = [lookup_documents, *sql_tools, search_google_shopping]  # save search token
# model = get_chat_prompt(use_hub=False) | llm.bind_tools(tools=tools)

# # Build graph
# graph_builder = StateGraph(State)

# # Node
# graph_builder.add_node("assistant", Assistant(model))
# graph_builder.add_node("tools", create_tool_node_with_fallback(tools))

# # Logic edges
# graph_builder.add_edge(START, "assistant")
# graph_builder.add_conditional_edges("assistant", tools_condition)
# graph_builder.add_edge("tools", "assistant")
# # End node decide by assistant itself

# # Compile graph with memory checkpoint
# graph_agent = graph_builder.compile(
#     checkpointer=memory,
#     # interrupt_before=["tools"]
# )

# --- GRAPH AGENT - before use prebuilt create_react_agent ---
# ------------------------------------------------------------

# GRAPH:
# https://mermaid.ink/img/pako:eNp9kt9uwiAUxl-FsDStiXXOi12g8co32K62LgTpQUgoNBQ0pum7j7pam6jj6juH74Mff1rMbQmY4CRplVGeoDYV2p64ZM6nfcWDO0JUqVYGmEu7rkuSwhwcqyX63K0Lg4ZBaeNjitLse1Nvx2rzWm9_ZoQQoVzjb3bWNCpajM9GNbvNumCot1ZnVzGZk6Fihjo4KjhRE_mzu85sigWmHKEuekTSbEo0IqM839741vdUTw1jD-WLaBn2e264A1__c8y_yKNtn1ivuBMnj0dudiBQCYIF7ZFQWpMXsRJLIeb9G-cS1EF68rZYPYhdHvESym3NuPJnsnxg6y92WHov9u-C4zmuwFVMlfGztX2iwF5CBQUmUQ40BS5MF60sePtxNhwT7wLMsbPhIDERTDexCnXJPOwUi5-wGrs1M1_WXuvuF4dU6-o