import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app.rag import ingest_documents


if __name__ == "__main__":
    ingest_documents()