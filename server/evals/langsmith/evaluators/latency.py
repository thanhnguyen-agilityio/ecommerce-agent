from langchain_openai import ChatOpenAI
from langsmith.schemas import Example, Run

gpt_4o_mini = ChatOpenAI(model="gpt-4o-mini")
gpt_3_5_turbo = ChatOpenAI(model="gpt-3.5-turbo")

# Set model for evaluation
model_evals = gpt_4o_mini


def latency_evaluator(root_run: Run, example: Example):
    """
    Evaluate the latency of the agent response.
    """
    latency = root_run.end_time - root_run.start_time
    return {"score": latency.total_seconds(), "key": "latency"}
