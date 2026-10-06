import os

from dotenv import load_dotenv
from groq import Groq


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ==========================================
# MODEL
# ==========================================

MODEL_NAME = "openai/gpt-oss-20b"


# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are RealEstateAI, an AI real estate assistant.

Your role is to help users understand real estate properties,
property prices, buying considerations, market trends,
and general real estate concepts.

You should:

1. Give clear and easy-to-understand answers.
2. Explain real estate terminology when needed.
3. Help users compare property options.
4. Discuss factors that can affect property prices.
5. Provide general buying guidance.
6. Never claim that a property is guaranteed to increase in value.
7. Clearly state when information is general guidance rather
   than professional legal or financial advice.
8. Do not invent specific property listings or market statistics.
9. Keep responses practical and concise.
"""


# ==========================================
# AI ASSISTANT FUNCTION
# ==========================================

def ask_real_estate_assistant(user_question):

    response = client.chat.completions.create(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_question
            }
        ],

        temperature=0.3,

        max_tokens=800
    )

    return response.choices[0].message.content