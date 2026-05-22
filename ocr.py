import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OCR_SPACE_API_KEY")


def extract_text(image_path: str) -> str:

    with open(image_path, "rb") as image_file:

        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={
                "filename": image_file
            },
            data={
                "apikey": API_KEY,
                "language": "eng",
                "OCREngine": 2,
                "isTable": True,
                "scale": True,
            }
        )

    result = response.json()

    if result.get("IsErroredOnProcessing"):
        raise Exception(result.get("ErrorMessage"))

    parsed_results = result.get("ParsedResults")

    if not parsed_results:
        return ""

    return parsed_results[0]["ParsedText"]
