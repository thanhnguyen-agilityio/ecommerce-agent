import random

import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.messages import ChatMessage
from services.chat_service import ChatService
from utils.constants import WELCOME_MESSAGE
from utils.utils import convert_chat_message, render_message

expander = st.expander("Quick Start:")
expander.write(
    """
    👉 Services:
    - Give me list categories
    - Do you offer free shipping?

    👉 Products:
    - Give me product "Serge Checkered Wide-Leg Pants"
    - Compare "Long Sleeves Tencel Shirt" with "Sleeves Style Shirt"
    - Do you have "Regular Striped Shirt" in size L?
    - Do you have "Bloom T-shirt" in size M?
    - Give me some products in category "Jackets".

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
        history.messages = [
            convert_chat_message(message["type"], message["content"])
            for message in messages
        ]
    except Exception:
        pass

# Show history messages to UI
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

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                response = chat_service.chat_stream(prompt)
                st.write_stream(response)
            except Exception as e:
                st.error(str(e))
                st.stop()
