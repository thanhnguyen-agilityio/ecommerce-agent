from agent.rag.retriever import get_retriever
from langchain_core.documents import Document
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    query: str

    service_categories: list[str] = Field(
        max_length=2,
        min_length=0,
    )

    # For test retry tool: uncomment below code
    # Only allow 1 categories, if model give 2, it will retry to have only 1 categories
    # Test query: "What are Shipping cost payment methods?" -> model will give 2 categories: faqs, policies
    # service_categories: list[str] = Field(
    #     max_length=1, min_length=0,
    # )


@tool
def lookup_documents(document_request: DocumentRequest) -> list[Document]:
    """
    Retrieve shop documents for queries about store services like policies, FAQs, or categories. Use for intent `service`.

    Categories:
    - faqs: General queries like "How to cancel an order."
    - policies: Detailed policy inquiries like "What is your refund policy?"

    Example:
    - Query: "What are your policies?" → Category: [policies]

    Use only when `intent = service`.
    """
    query = document_request.query
    service_categories = document_request.service_categories
    docs = []
    doc_ids = set()

    for category in service_categories:
        retriever = get_retriever(service_category=category)
        category_docs = retriever.invoke(query)

        if category_docs:
            for doc in category_docs:
                if doc.id not in doc_ids:
                    doc_ids.add(doc.id)
                    docs.append(doc)

    return docs
