import sys
import os


# Add project root to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from app.ai_assistant import ask_real_estate_assistant


question = """
What are the most important factors to consider
before buying a house?
"""


print("\n========== AI REAL ESTATE ASSISTANT ==========\n")

answer = ask_real_estate_assistant(question)

print(answer)

print("\n==============================================")