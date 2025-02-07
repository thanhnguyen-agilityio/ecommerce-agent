import random

from langchain_core.messages import ChatMessage
from streamlit import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from utils.constants import BOT_AVATAR_CHOICE, USER_AVATAR_CHOICE

USER_AVATAR = random.choice(USER_AVATAR_CHOICE)
BOT_AVATAR = random.choice(BOT_AVATAR_CHOICE)


def get_session_id():
    return get_script_run_ctx().session_id


def convert_chat_message(type, content):
    match type:
        case "human":
            return ChatMessage(role="user", content=content)
        case "ai":
            return ChatMessage(role="assistant", content=content)
        case _:
            return ChatMessage(role="unknown", content=content)


def get_chat_message_avatar(msg):
    match msg.role:
        case "user":
            return "👤"
        case "assistant":
            return "🤖"
        case _:
            return "🤔"


def render_message(msg):
    avatar = None

    match msg.role:
        case "user":
            avatar = USER_AVATAR

        case "assistant":
            avatar = BOT_AVATAR
        case _:
            avatar = "🤔"

    if avatar and avatar != "🤔":
        message = st.chat_message(msg.role, avatar=avatar)
        message.markdown(msg.content)
