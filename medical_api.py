from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_medical_insights(raw_text: str):

    cleaned_text = raw_text[:15000]
    system_prompt = """
You are a concise AI medical insight assistant.

Analyze OCR extracted lab reports.

STRICT RULES:
- Maximum 60 words
- Maximum 4 bullet points
- VERY SHORT response
- No tables
- No markdown headings
- No detailed explanations
- No medical essay
- No repeating lab values excessively
- No diagnosis
- No treatment plans
- No long recommendations

Focus ONLY on:
- abnormal findings
- important observations
- possible concern indicators

Response style example:

• Hemoglobin appears low suggesting possible anemia  
• Fever indicators detected  
• Body weight appears below normal range  
• Doctor follow-up recommended for further evaluation

Keep output compact and mobile-friendly.
"""

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            temperature=0.2,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""
MEDICAL OCR TEXT:
----------------------
{cleaned_text}
----------------------
"""
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        print("Medical Insight Error:", str(e))

        return "Unable to generate medical insights."


