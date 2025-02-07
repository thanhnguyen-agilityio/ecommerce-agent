import utils.constants as constants
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def init_chat_model(model_name, temperature, streaming=False, callbacks=None):
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        streaming=streaming,
        callbacks=callbacks,
    )


model = ChatOpenAI(model=constants.CHAT_MODEL)
embeddings_model = OpenAIEmbeddings(
    model=constants.EMBEDDING_MODEL,
)
