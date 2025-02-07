import json
import os
import time


def load_json(file_path: str):
    if not file_path or file_path.lower().endswith(".json") is False:
        print(f"Invalid file path: {file_path}")
        return

    with open(os.path.abspath(file_path), "rb") as file:
        try:
            return json.loads(file.read())
        except json.JSONDecodeError:
            print(f"Error decoding JSON file: {file_path}")
            return


def get_path(file_name: str, folder: str = "."):
    return os.path.abspath(f"{folder}/{file_name}")


def is_chroma_db_exist(persist_directory: str) -> bool:
    # Check if the directory exists
    if not os.path.exists(persist_directory):
        return False

    # Check for specific metadata files used by Chroma
    required_files = ["chroma.sqlite3"]
    for file in required_files:
        if not os.path.exists(os.path.join(persist_directory, file)):
            return False

    return True


def count_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time for {func.__name__}: {end_time - start_time} seconds")
        return result

    return wrapper


# ----- LangGraph Utils - before use prebuilt create_react_agent -----
# from langchain_core.messages import ToolMessage
# from langchain_core.runnables import RunnableLambda
# from langgraph.prebuilt import ToolNode

# def handle_tool_error(state) -> dict:
#     error = state.get("error")
#     tool_calls = state["messages"][-1].tool_calls
#     return {
#         "messages": [
#             ToolMessage(
#                 content=f"Error: {repr(error)}\n please fix your mistakes.",
#                 tool_call_id=tc["id"],
#             )
#             for tc in tool_calls
#         ]
#     }


# def create_tool_node_with_fallback(tools: list) -> dict:
#     return ToolNode(tools).with_fallbacks(
#         [RunnableLambda(handle_tool_error)], exception_key="error"
#     )

# ----- LangGraph Utils - before use prebuilt create_react_agent -----
