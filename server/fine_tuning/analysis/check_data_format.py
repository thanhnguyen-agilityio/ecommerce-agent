import json
from collections import defaultdict

# Data loading
data_path = "server/fine_tuning/data/v2/fine_tuning/ivy_fine_tuning_data_v2.jsonl"

# Load the dataset
with open(data_path, "r", encoding="utf-8") as f:
    dataset = []
    for line in f:
        try:
            dataset.append(json.loads(line))
        except Exception as e:
            print("line::::", line)
            raise e

# Initial dataset stats
print("Num examples:", len(dataset))
print("First example:")
for message in dataset[0]["messages"]:
    print(message)

# Format validation
# Format error checks
format_errors = defaultdict(int)

for ex in dataset:
    if not isinstance(ex, dict):
        format_errors["data_type"] += 1
        continue

    messages = ex.get("messages", None)
    if not messages:
        format_errors["missing_messages_list"] += 1
        continue

    for message in messages:
        if "role" not in message or "content" not in message:
            format_errors["message_missing_key"] += 1

        if any(
            k not in ("role", "content", "name", "function_call", "weight")
            for k in message
        ):
            format_errors["message_unrecognized_key"] += 1

        if message.get("role", None) not in ("system", "user", "assistant", "function"):
            format_errors["unrecognized_role"] += 1

        content = message.get("content", None)
        function_call = message.get("function_call", None)

        if (not content and not function_call) or not isinstance(content, str):
            format_errors["missing_content"] += 1

    if not any(message.get("role", None) == "assistant" for message in messages):
        format_errors["example_missing_assistant_message"] += 1

if format_errors:
    print("Found errors:")
    for k, v in format_errors.items():
        print(f"{k}: {v}")
else:
    print("No errors found")


# Ref: https://cookbook.openai.com/examples/chat_finetuning_data_prep
