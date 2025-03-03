import sqlite3

import utils.constants as constants
from agent.llms import init_chat_model
from agent.prompts.prompt import get_chat_prompt, get_system_message
from agent.tools import (
    safe_tools,
    sensitive_tool_names,
    sensitive_tools,
    tools_mapping
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.store.memory import InMemoryStore
from utils.utils import create_tool_node_with_fallback, get_path

# Initialize store, memory, and cache
store = InMemoryStore()
memory = SqliteSaver(
    sqlite3.connect(get_path("checkpoints.sqlite", "db"), check_same_thread=False)
)
set_llm_cache(SQLiteCache(database_path="db/ecommerce_chatbot_cache.db"))


class State(MessagesState):
    pass


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        result = self.runnable.invoke(state)
        return {"messages": result}


def create_assistant_runnable(chat_model, config):
    if not config:
        raise ValueError("config is required to create assistant runnable")

    # Config model with tool calling
    chat_model_bind_tools = chat_model.bind_tools(tools=list(tools_mapping.values()))

    # Config system prompt
    memories = []
    system_message = get_system_message(use_hub=False)
    # retrieve user memories and add them to the system message
    user_id = config.get("configurable", {}).get("user_id")
    namespace = ("memories", user_id)
    memories = [m.value["data"] for m in store.search(namespace)]

    return get_chat_prompt(system_message, memories) | chat_model_bind_tools


def route_tools(state: State):
    """
    Route tools from assistant node based on the tool name.
    - If next node is END, return END.
    - If the tool name is in sensitive_tool_names, route to sensitive_tools node.
    - Otherwise, route to safe_tools node.
    """
    next_node = tools_condition(state)

    if next_node == END:
        return END

    ai_message = state["messages"][-1]
    for tool_call in ai_message.tool_calls:
        if tool_call["name"] in sensitive_tool_names:
            return "sensitive_tools"

    return "safe_tools"


def init_graph(
    model_name=constants.CHAT_MODEL,
    temperature=constants.CHAT_MODEL_TEMPERATURE,
    streaming=True,
    config=None,
):
    # Prepare nodes
    chat_model = init_chat_model(
        model_name=model_name,
        temperature=temperature,
        streaming=streaming,
        callbacks=([StreamingStdOutCallbackHandler()] if streaming else []),
    )
    node_assistant = Assistant(create_assistant_runnable(chat_model, config))
    node_safe_tools = create_tool_node_with_fallback(safe_tools)
    node_sensitive_tools = create_tool_node_with_fallback(sensitive_tools)

    # Build graph
    builder = StateGraph(State)
    # - add nodes
    builder.add_node("assistant", node_assistant)
    builder.add_node("safe_tools", node_safe_tools)
    builder.add_node("sensitive_tools", node_sensitive_tools)

    # - define edges
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        route_tools,
        ["safe_tools", "sensitive_tools", END]
    )
    builder.add_edge("safe_tools", "assistant")
    builder.add_edge("sensitive_tools", "assistant")
    graph_agent = builder.compile(
        checkpointer=memory,
        store=store,
        interrupt_before=["sensitive_tools"],
        debug=True,
    )

    # For testing graph visualization
    # print(graph_agent.get_graph().draw_mermaid())
    return graph_agent