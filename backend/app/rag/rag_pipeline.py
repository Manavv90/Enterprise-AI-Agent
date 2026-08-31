from backend.app.rag.embeddings import create_embeddings
from backend.app.rag.vector_store import search_documents
from backend.app.services.llm_service import generate_response


SIMILARITY_THRESHOLD = 1.60


def answer_question(
    query: str,
    top_k: int = 3,
    source: str | None = None
) -> dict:
    """
    Answer a question using relevant document context.
    """

    # Create embedding for the user's question
    query_embedding = create_embeddings([query])[0]

    # Retrieve relevant document chunks
    results = search_documents(
        query_embedding,
        top_k=top_k,
        source=source
    )

    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]

    # Keep only sufficiently relevant chunks
    relevant_documents = [
        document
        for document, distance in zip(documents, distances)
        if distance <= SIMILARITY_THRESHOLD
    ]

    if not relevant_documents:
        return {
            "response": (
                "I could not find this information "
                "in the provided documents."
            ),
            "sources": []
        }

    # Combine relevant chunks
    context = "\n\n".join(relevant_documents)

    # Create grounded prompt
    prompt = f"""
You are an enterprise AI assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context, say:
"I could not find this information in the provided documents."

Do not invent or assume information.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    response = generate_response(prompt)

    # Get unique sources from relevant chunks
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