# ruff: noqa: E741
import json

from utils import (
    num_assistant_tokens_from_messages,
    num_tokens_from_messages,
    print_distribution,
)

# Data loading
data_path = "server/fine_tuning/data/ivy_chat_fine_tuning.jsonl"

# Load the dataset
with open(data_path, "r", encoding="utf-8") as f:
    dataset = [json.loads(line) for line in f]


# Warnings and tokens counts
n_missing_system = 0
n_missing_user = 0
n_messages = []
convo_lens = []
assistant_message_lens = []

for ex in dataset:
    messages = ex["messages"]
    if not any(message["role"] == "system" for message in messages):
        n_missing_system += 1
    if not any(message["role"] == "user" for message in messages):
        n_missing_user += 1
    n_messages.append(len(messages))
    convo_lens.append(num_tokens_from_messages(messages))
    assistant_message_lens.append(num_assistant_tokens_from_messages(messages))

print("Num examples missing system message:", n_missing_system)
print("Num examples missing user message:", n_missing_user)
print_distribution(n_messages, "num_messages_per_example")
print_distribution(convo_lens, "num_total_tokens_per_example")
print_distribution(assistant_message_lens, "num_assistant_tokens_per_example")
n_too_long = sum(l > 16385 for l in convo_lens)
print(
    f"\n{n_too_long} examples may be over the 16,385 token limit, they will be truncated during fine-tuning"
)
