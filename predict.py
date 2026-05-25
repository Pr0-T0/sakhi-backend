import pandas as pd
import joblib

from models import InsightRequest

# Load once during startup
model = joblib.load("insight_model.pkl")
scaler = joblib.load("scaler.pkl")

FEATURE_COLUMNS = [
    "avg_nutrition_score",
    "avg_toxicity_score",
    "avg_processed_score",
    "avg_hormonal_score",
    "avg_overall_score",
    "scan_frequency_weekly",
    "scan_count",
    "healthy_scan_ratio",
    "high_toxicity_ratio",
    "cosmetic_ratio",
    "food_ratio"
]


def predict_insights(data: InsightRequest):

    # Convert request -> dataframe
    df = pd.DataFrame([data.dict()])

    # Ensure exact feature order
    df = df[FEATURE_COLUMNS]

    # Scale features
    scaled = scaler.transform(df)

    # Predict probabilities
    probs = model.predict_proba(scaled)[0]

    # Map labels -> probabilities
    result = dict(zip(model.classes_, probs))

    # Sort highest confidence first
    sorted_probs = sorted(
        result.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # Filter weak predictions
    predictions = [
        {
            "label": label,
            "confidence": round(float(prob), 4)
        }
        for label, prob in sorted_probs
    ]

    return {
        "predictions": predictions
    }
