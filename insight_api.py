from groq import Groq
from dotenv import load_dotenv

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_insight(predictions: list):

    system_prompt = """
You are a wellness insight assistant.

Generate concise, informative wellness insights from behavioral prediction data.

RULES:
- 2 to 4 sentences
- Friendly and informative tone
- Do NOT mention confidence percentages
- Do NOT sound overly medical
- Do NOT diagnose diseases
- Explain possible wellness implications
- Mention positive and negative patterns if relevant
"""

    formatted_predictions = "\n".join(
        [
            f"- {item['label']}: {item['confidence']}%"
            for item in predictions
        ]
    )

    user_prompt = f"""
Behavioral predictions:

{formatted_predictions}

Generate a wellness insight.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
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
        temperature=0.7,
        max_tokens=180
    )

    return response.choices[0].message.content
