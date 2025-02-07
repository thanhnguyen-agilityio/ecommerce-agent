import json

from utils import num_tokens_from_messages

# Data loading
data_path = "server/fine_tuning/data/ivy_chat_fine_tuning.jsonl"

# Load the dataset
with open(data_path, "r", encoding="utf-8") as f:
    dataset = [json.loads(line) for line in f]

convo_lens = []
for ex in dataset:
    messages = ex["messages"]
    convo_lens.append(num_tokens_from_messages(messages))


# Pricing and default n_epochs estimate
MAX_TOKENS_PER_EXAMPLE = 16385

TARGET_EPOCHS = 3
MIN_TARGET_EXAMPLES = 100
MAX_TARGET_EXAMPLES = 25000
MIN_DEFAULT_EPOCHS = 1
MAX_DEFAULT_EPOCHS = 25

n_epochs = TARGET_EPOCHS
n_train_examples = len(dataset)
if n_train_examples * TARGET_EPOCHS < MIN_TARGET_EXAMPLES:
    n_epochs = min(MAX_DEFAULT_EPOCHS, MIN_TARGET_EXAMPLES // n_train_examples)
elif n_train_examples * TARGET_EPOCHS > MAX_TARGET_EXAMPLES:
    n_epochs = max(MIN_DEFAULT_EPOCHS, MAX_TARGET_EXAMPLES // n_train_examples)

n_billing_tokens_in_dataset = sum(
    min(MAX_TOKENS_PER_EXAMPLE, length) for length in convo_lens
)
print(
    f"Dataset has ~{n_billing_tokens_in_dataset} tokens that will be charged for during training"
)
print(f"By default, you'll train for {n_epochs} epochs on this dataset")
print(
    f"By default, you'll be charged for ~{n_epochs * n_billing_tokens_in_dataset} tokens"
)
