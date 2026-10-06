import os
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# RAG documents folder
DOCUMENTS_DIR = BASE_DIR / "rag_documents"

# ChromaDB storage
CHROMA_DIR = BASE_DIR / "chroma_db"

# Collection name
COLLECTION_NAME = "real_estate_knowledge"


# Embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# ChromaDB client
chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


# Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )

groq_client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-20b"


def read_document(file_path):
    """Read text from TXT or PDF files."""

    if file_path.suffix.lower() == ".txt":

        return file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    elif file_path.suffix.lower() == ".pdf":

        reader = PdfReader(str(file_path))

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    return ""


def split_text(text, chunk_size=800, overlap=100):
    """Split document text into overlapping chunks."""

    text = " ".join(text.split())

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


def ingest_documents():
    """Load documents and store embeddings in ChromaDB."""

    documents = []
    metadatas = []
    ids = []

    files = list(DOCUMENTS_DIR.glob("*.txt"))
    files += list(DOCUMENTS_DIR.glob("*.pdf"))

    if not files:

        print(
            "No documents found in rag_documents folder."
        )

        return

    print(
        f"Found {len(files)} document(s)."
    )

    for file_path in files:

        print(
            f"Reading: {file_path.name}"
        )

        text = read_document(file_path)

        if not text.strip():

            print(
                f"Skipping empty document: {file_path.name}"
            )

            continue

        chunks = split_text(text)

        print(
            f"  Created {len(chunks)} chunks."
        )

        for i, chunk in enumerate(chunks):

            documents.append(chunk)

            metadatas.append({
                "source": file_path.name,
                "chunk": i
            })

            ids.append(
                f"{file_path.stem}_{i}"
            )

    if not documents:

        print(
            "No usable text found."
        )

        return

    print(
        "Creating embeddings..."
    )

    embeddings = embedding_model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    print(
        "Saving documents to ChromaDB..."
    )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        "\nRAG ingestion completed successfully!"
    )

    print(
        f"Total chunks stored: {collection.count()}"
    )


def search_documents(query, top_k=3):
    """Retrieve the most relevant document chunks."""

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results


def ask_rag_assistant(query, top_k=3):
    """
    Retrieve relevant documents and generate
    an answer using Groq.
    """

    results = search_documents(
        query,
        top_k=top_k
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    if not documents:

        return {
            "answer": (
                "I could not find relevant information "
                "in the knowledge base."
            ),
            "sources": []
        }

    context_parts = []

    for document in documents:

        context_parts.append(
            document
        )

    context = "\n\n".join(
        context_parts
    )

    system_prompt = """
You are RealEstateAI, a helpful real estate
knowledge assistant.

Answer the user's question using ONLY the
provided knowledge base context.

If the answer is not available in the context,
clearly say that the information is not available
in the knowledge base.

Do not invent property listings, prices,
statistics, laws, or facts.

For legal, financial, or property-documentation
questions, provide general educational information
and recommend consulting an appropriate qualified
professional when necessary.

Keep answers clear, useful, and easy to understand.
"""

    user_prompt = f"""
Knowledge Base Context:

{context}

User Question:

{query}

Answer the question using the knowledge base.
"""

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    answer = response.choices[0].message.content

    sources = []

    for metadata in metadatas:

        source = metadata.get(
            "source"
        )

        if source and source not in sources:

            sources.append(source)

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":

    ingest_documents()