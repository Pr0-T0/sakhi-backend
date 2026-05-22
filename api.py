from typing import List, Optional, Literal
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import instructor
import os

# -----------------------------------
# Environment
# -----------------------------------

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

client = instructor.from_groq(
    groq_client,
    mode=instructor.Mode.JSON
)

# -----------------------------------
# Nutrition Models
# -----------------------------------

class NutritionValue(BaseModel):

    value: Optional[float] = None

    unit: Optional[str] = None


class NutritionFacts(BaseModel):

    serving_size: Optional[str] = None

    calories: Optional[NutritionValue] = None

    sugar: Optional[NutritionValue] = None

    added_sugar: Optional[NutritionValue] = None

    protein: Optional[NutritionValue] = None

    fat: Optional[NutritionValue] = None

    saturated_fat: Optional[NutritionValue] = None

    trans_fat: Optional[NutritionValue] = None

    sodium: Optional[NutritionValue] = None

    fiber: Optional[NutritionValue] = None

    carbohydrates: Optional[NutritionValue] = None


# -----------------------------------
# Ingredient Models
# -----------------------------------

class Ingredient(BaseModel):

    original_text: str

    normalized_name: str

    ingredient_type: Optional[
        Literal[
            "Preservative",
            "Fragrance",
            "Colorant",
            "Sweetener",
            "Surfactant",
            "Emulsifier",
            "Oil",
            "Herbal Extract",
            "Vitamin",
            "Mineral",
            "Unknown"
        ]
    ] = "Unknown"

    risk_tags: List[str] = []

    detected_edc: bool = False

    is_natural: Optional[bool] = None


# -----------------------------------
# Main Extraction Model
# -----------------------------------

class OCRAnalysis(BaseModel):

    document_type: Literal[
        "Product / Cosmetic Label",
        "Packaged Food Label",
        "Supplement Label",
        "Unknown"
    ]

    product_name: Optional[str] = None

    brand_name: Optional[str] = None

    product_category: Optional[str] = None

    ingredients: List[Ingredient] = []

    nutrition: Optional[NutritionFacts] = None

    claims: List[str] = []

    allergens: List[str] = []

    preservatives_detected: List[str] = []

    artificial_additives: List[str] = []

    fragrance_detected: bool = False

    has_nutrition_table: bool = False

    has_ingredient_list: bool = False

    ocr_quality: Literal[
        "good",
        "moderate",
        "poor"
    ] = "moderate"

    warnings: List[str] = []

    notes: Optional[str] = None


# -----------------------------------
# Extraction Function
# -----------------------------------

def extract_structured_data(raw_text: str):

    cleaned_text = raw_text[:15000]

    system_prompt = """
You are a STRICT OCR product intelligence extraction engine.

Your ONLY job:
Extract structured factual information from OCR text.

IMPORTANT:
- NEVER generate explanations
- NEVER generate toxicity scores
- NEVER generate hormonal scores
- NEVER generate health advice
- NEVER hallucinate ingredients
- NEVER hallucinate nutrition values
- ONLY extract visible information
- Normalize OCR spelling mistakes carefully
- Preserve ingredient meaning accurately

Your goal is to extract ALL information useful for:
- toxicity analysis
- endocrine disruption analysis
- hormonal health analysis
- nutrition analysis
- processed food analysis

You MUST detect:
- product name
- brand
- ingredients
- preservatives
- fragrances
- artificial additives
- sweeteners
- colors
- surfactants
- nutrition values
- allergens
- product claims

Mark detected_edc=true ONLY if ingredient clearly belongs to:
- Parabens
- Phthalates
- Sulfates
- BPA
- PFAS
- Synthetic Fragrance
- Heavy Metals

Examples:
- Parfum -> Fragrance
- SLS -> Surfactant
- SLES -> Surfactant
- BHT -> Preservative
- Sodium Benzoate -> Preservative

Extract nutrition values carefully.

If a nutrition table exists:
- detect units properly
- map nutrients correctly
"""

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            temperature=0,

            response_model=OCRAnalysis,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""
OCR TEXT:
-------------------
{cleaned_text}
-------------------
"""
                }
            ]
        )

        return response

    except Exception as e:

        print("Groq Extraction Error:", str(e))

        return OCRAnalysis(
            document_type="Unknown",
            warnings=["Extraction failed"],
            notes=str(e)
        )
