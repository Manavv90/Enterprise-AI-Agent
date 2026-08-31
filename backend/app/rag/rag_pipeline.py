import re
from backend.app.services.memory_service import (
    add_message,
    get_history
)

from backend.app.rag.embeddings import create_embeddings
from backend.app.rag.vector_store import search_documents
from backend.app.services.llm_service import generate_response


SIMILARITY_THRESHOLD = 1.60
def extract_company_from_source(source: str) -> str | None:
    """
    Extract company name from a document filename.
    """

    if not source:
        return None

    match = re.search(
        r"-\s*([A-Za-z0-9&.\s]+)\.pdf$",
        source,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return None


def answer_question(
    query: str,
    top_k: int = 3,
    source: str | None = None,
    session_id: str = "default"
) -> dict:
    """
    Answer a question using relevant document context
    and conversation history.
    """

    # Get previous conversation
    history = get_history(session_id)

    conversation = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in history[-6:]
    )
    # Handle company questions directly from the document source
    company_keywords = [
        "which company",
        "what company",
        "company is this",
        "which organization",
        "what organization"
    ]

    if source and any(
        keyword in query.lower()
        for keyword in company_keywords
    ):
        company = extract_company_from_source(source)

        if company:
            response = f"The position is for {company}."

            add_message(session_id, "user", query)
            add_message(session_id, "assistant", response)

            return {
                "response": response,
                "sources": [source]
            }
    # Build retrieval query using conversation context
    if history:
        retrieval_query = f"""
Previous conversation:
{conversation}

Current question:
{query}
"""
    else:
        retrieval_query = query

    # Create embedding
    query_embedding = create_embeddings([retrieval_query])[0]

    # Retrieve relevant document chunks
    results = search_documents(
        query_embedding,
        top_k=top_k,
        source=source
    )

    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]

    # Keep sufficiently relevant chunks
    relevant_documents = [
        document
        for document, distance in zip(documents, distances)
        if distance <= SIMILARITY_THRESHOLD
    ]

    # If no relevant chunks were found
    if not relevant_documents:

        # If a specific document was selected,
        # allow the source filename to help answer
        # questions about the selected document.
        if source:
            source_context = f"Document source: {source}"

            prompt = f"""
You are an enterprise AI assistant.

The user has explicitly selected the following document:

DOCUMENT SOURCE:
{source_context}

CONVERSATION HISTORY:
{conversation}

CURRENT QUESTION:
{query}

If the question asks which company, organization,
or document a position is associated with, you may
identify it from the document source filename.

Otherwise, answer only if the information can be
determined from the selected document or conversation.

Do not invent information.

If the answer cannot be determined, say:
"I could not find this information in the provided documents."

ANSWER:
"""

            response = generate_response(prompt)

            add_message(session_id, "user", query)
            add_message(session_id, "assistant", response)

            return {
                "response": response,
                "sources": [source]
            }

        return {
            "response": (
                "I could not find this information "
                "in the provided documents."
            ),
            "sources": []
        }

    # Combine relevant chunks
    context = "\n\n".join(relevant_documents)

    # Include document source information
    source_context = "\n".join(
        f"Document source: {metadata.get('source')}"
        for metadata, distance in zip(metadatas, distances)
        if distance <= SIMILARITY_THRESHOLD
        and metadata.get("source")
    )

    # Create grounded prompt
    prompt = f"""
You are an enterprise AI assistant.

Answer the user's question using ONLY the information
provided in the context below.

Use the conversation history to understand references
such as "this company", "that position", or "what about it".

The document source name may be used to identify
which uploaded document the context came from.

If the answer cannot be found in the context or
identified from the document source, say:
"I could not find this information in the provided documents."

Do not invent or assume information.

CONVERSATION HISTORY:
{conversation}

DOCUMENT SOURCE:
{source_context}

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    # Generate answer
    response = generate_response(prompt)

    # Save conversation
    add_message(session_id, "user", query)
    add_message(session_id, "assistant", response)

    # Get unique sources
    sources = list({
        metadata.get("source")
        for metadata, distance in zip(metadatas, distances)
        if distance <= SIMILARITY_THRESHOLD
        and metadata.get("source")
    })

    return {
        "response": response,
        "sources": sources
    }

