import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app.rag import ask_rag_assistant


question = (
    "What should I check before buying a house?"
)

print("\nUser Question:")
print(question)

print("\nGenerating RAG answer...\n")

result = ask_rag_assistant(question)

print("Answer:")
print(result["answer"])

print("\nSources:")

for source in result["sources"]:
    print(f"- {source}")