import random

import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.messages import ChatMessage
from services.chat_service import ChatService
from utils.constants import BOT_AVATAR, WELCOME_MESSAGE
from utils.utils import convert_chat_message, render_message

expander = st.expander("Quick Start:")
expander.write(
    """
    👉 Services:
    - Give me list categories
    - Do you offer free shipping?

    👉 Products:
    - Give me product "Dreamy Styled Collar Shirt"
    - Compare "Straight Cut Button-down Collar Shirt" with "DIVAS Polo T-shirt"
    - Do you have "Magnolia Tuytsi Blazer" in size L?
    - Give me some products in category "jacket".

    👉 FAQs:
    - How can I maintain the shape of my clothing?

    🎯 Tip: short and specific.
    """
)

# Initialize chat service
chat_service = ChatService(
    user_id=st.session_state.user_id,
    thread_id=st.session_state.thread_id,
)

# load history messages from Streamlit session state
history = StreamlitChatMessageHistory(
    key=f"user_{st.session_state.user_id}_chat_messages"
)

# Get chat history of thread_id
with st.spinner("Loading..."):
    try:
        messages = chat_service.chat_history()
        history_message_convert = []
        for message in messages:
            message_convert = convert_chat_message(message["type"], message["content"])
            # print("message_convert: ", message_convert)
            if message_convert:
                history_message_convert.append(message_convert)

        history.messages = history_message_convert
    except Exception:
        pass

# Show history messages to UI
# print("history.messages: ", history.messages)
for msg in history.messages:
    render_message(msg)

# Initialize welcome message
if len(history.messages) == 0:
    chat_message = ChatMessage(role="assistant", content=random.choice(WELCOME_MESSAGE))
    render_message(chat_message)
    history.add_message(chat_message)


# Handle user interaction
if prompt := st.chat_input(placeholder="Give me categories list."):
    chat_message = ChatMessage(role="user", content=prompt)
    render_message(chat_message)
    history.add_message(chat_message)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        try:
            response = chat_service.chat_stream(prompt)
            st.write_stream(response)
        except Exception as e:
            st.error(str(e))
            st.stop()
