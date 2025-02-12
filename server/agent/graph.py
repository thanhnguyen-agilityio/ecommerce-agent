import sqlite3

import utils.constants as constants
from agent.llms import init_chat_model
from agent.prompts.prompt import get_chat_prompt, get_system_message
from agent.tools.lookup_documents import lookup_documents
from agent.tools.save_memory import save_memory
from agent.tools.search_google_shopping import search_google_shopping
from agent.tools.sql_tools import (
    check_and_execute_query_tool,
    sql_db_list_tables,
    sql_db_schema,
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from utils.utils import get_path

store = InMemoryStore()
tools = [
    save_memory,
    lookup_documents,
    sql_db_schema,
    sql_db_list_tables,
    check_and_execute_query_tool,
    search_google_shopping,
]
set_llm_cache(SQLiteCache(database_path="db/ecommerce_chatbot_cache.db"))


def prepare_model_inputs(state: AgentState, config: RunnableConfig, store: BaseStore):
    # Retrieve user memories and add them to the system message
    # This function is called **every time** the model is prompted. It converts the state to a prompt
    user_id = config.get("configurable", {}).get("user_id")
    namespace = ("memories", user_id)
    memories = [m.value["data"] for m in store.search(namespace)]
    system_message = get_system_message(use_hub=False)
    return get_chat_prompt(system_message, memories)


def init_graph(
    model_name=constants.CHAT_MODEL,
    temperature=constants.CHAT_MODEL_TEMPERATURE,
    streaming=True,
):
    chat_model = init_chat_model(
        model_name=model_name,
        temperature=temperature,
        streaming=streaming,
        callbacks=([StreamingStdOutCallbackHandler()] if streaming else []),
    )

    # Save checkpoint to sqlite db
    conn = sqlite3.connect(
        get_path("checkpoints.sqlite", "db"), check_same_thread=False
    )
    memory = SqliteSaver(conn)
    graph_agent = create_react_agent(
        chat_model,
        tools=tools,
        state_modifier=prepare_model_inputs,
        store=store,
        checkpointer=memory,
        # debug=True,
    )

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
