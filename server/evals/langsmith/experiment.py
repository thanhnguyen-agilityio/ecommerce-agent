import os
import sys
import uuid

from langsmith import Client, evaluate

# CONFIG PATH WHEN RUN SCRIPT (via Python runner in Promptfoo) TO ALLOW IMPORT MODULE FROM ROOT DIR
# ----------------------------------------------------------------
server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
for path in [server_path]:
    if path not in sys.path:
        sys.path.append(path)
# ----------------------------------------------------------------


from agent.graph import init_graph  # noqa: E402
from evaluators import (  # noqa: E402; is_concise_enough,
    compare_semantic_similarity,
    latency_evaluator,
)


def target_function(inputs: dict):
    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),
            "user_id": "user_eval_1",
        }
    }
    messages = [("user", inputs["user_query"])]
    graph = init_graph(config=config)
    response = graph.invoke({"messages": messages}, config)
    return response["messages"][-1].content


client = Client()
dataset_name = "ecommerce-agent-dataset-with-fine-tuned-model"
evaluate(
    target_function,
    data=dataset_name,
    evaluators=[compare_semantic_similarity, latency_evaluator],
    experiment_prefix="Ecommerce Agent Data Set Fine Tuning Experiment",
    num_repetitions=1,
)


# # TASK: Run 1 example with ID
# # "Ecommerce Golden Data Set"
# dataset_id = "12e5f450-fac3-4b2c-b167-4a80c1c6b386"
# # Give me list of policies
# example_id = "d5dd3bc6-3646-4f41-b63c-eaabd5d62e86"
# examples = client.list_examples(dataset_id=dataset_id)
# for example in examples:
#     if str(example.id) == example_id:
#         example_to_run = example
#         break

# evaluate(
#     target_function,
#     data=[example_to_run],
#     evaluators=[
#         compare_semantic_similarity,
#         is_concise_enough,
#         latency_evaluator
#     ],
#     experiment_prefix=f"Eval example {example_id}",
# )

# Need recheck: all product query is not correct
# Give me price of "Iphone 15"
# Compare "Viviane Pleated Fitted Dress" and "Pauline Neckline Fitted Dress".
# How much is the product "French Style Vest (with Croptop)"?
# Give me product "Lucille Silk Collared Shirt"
# Is "Sleeves Style Shirt" in stock?
