from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import tempfile
import os

from medical_api import generate_medical_insights
from news_api import get_food_news
from models import InputModel
from api import extract_structured_data
from ocr import extract_text
from score_engine import calculate_scores
from models import InsightRequest
from predict import predict_insights
from insight_api import generate_insight
app = FastAPI()

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)                   


@app.get("/")
def home():
    return {"message":"FastAPI server is running"}

from response_builder import build_scan_response

# -----------------------------------
# Endpoint
# -----------------------------------

@app.post("/extract-text")
async def extract_text_from_image(
    file: UploadFile = File(...)
):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    ) as temp_file:

        shutil.copyfileobj(
            file.file,
            temp_file
        )

        temp_path = temp_file.name

    try:

        # OCR
        extracted_text = extract_text(
            temp_path
        )

        # Structured extraction
        structured_data = extract_structured_data(
            extracted_text
        )

        extracted_dict = structured_data.model_dump()

        # Score engine
        score_data = calculate_scores(
            extracted_dict
        )

        # Final API response
        response = build_scan_response(
            filename=file.filename,
            extracted_data=extracted_dict,
            score_data=score_data
        )

        return response

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/scan-lab-report")
async def scan_lab_report(
    file: UploadFile = File(...)
):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    ) as temp_file:

        shutil.copyfileobj(
            file.file,
            temp_file
        )

        temp_path = temp_file.name

    try:

        extracted_text = extract_text(
            temp_path
        )
        insights = generate_medical_insights(extracted_text)  
        response = {
            "success": True,
            "filename": file.filename,
            "insights": insights,
        }

        return response

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)
@app.get("/food-news")
def food_news():

    return get_food_news()

@app.post("/predict-insights")
def predict(data: InsightRequest):
    result = predict_insights(data)
    insights = generate_insight(result["predictions"])
    return insights
