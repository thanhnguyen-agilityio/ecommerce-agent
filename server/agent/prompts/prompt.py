import logging

from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils.utils import get_path


def get_system_message(use_hub: bool = False):
    if use_hub:
        hub_prompt_template = hub.pull("ecommerce-agent-prompt")
        system_message = hub_prompt_template.messages[0].prompt.template
    else:
        try:
            system_message_file_path = get_path(
                "agent_prompt_with_fine_tuning_model_v2.md", "agent/prompts"
            )
            with open(system_message_file_path, "r") as f:
                system_message = f.read()
        except FileNotFoundError as e:
            logging.error(
                f"System message file at {system_message_file_path} not found!"
            )
            raise e

    return system_message


def get_chat_prompt(system_message: str, memories: list = None):
    system_message = get_system_message(use_hub=False)
    memories = memories or []
    return ChatPromptTemplate.from_messages(
        [
            ("system", f"{system_message}\n\nUser memories: {', '.join(memories)}"),
            ("placeholder", "{messages}"),
        ]
    )
