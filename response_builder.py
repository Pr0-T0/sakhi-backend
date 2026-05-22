# response_builder.py

from typing import Dict


# -----------------------------------
# Cleanup Utility
# -----------------------------------

def remove_empty(data):

    if isinstance(data, dict):

        cleaned = {}

        for key, value in data.items():

            value = remove_empty(value)

            if value not in (
                None,
                {},
                [],
                ""
            ):
                cleaned[key] = value

        return cleaned

    elif isinstance(data, list):

        cleaned = []

        for item in data:

            item = remove_empty(item)

            if item not in (
                None,
                {},
                [],
                ""
            ):
                cleaned.append(item)

        return cleaned

    return data


# -----------------------------------
# Response Builder
# -----------------------------------

def build_scan_response(
    *,
    filename: str,
    extracted_data: Dict,
    score_data: Dict
):

    response = {

        # -----------------------------------
        # STATUS
        # -----------------------------------

        "status": score_data.get(
            "status",
            "completed"
        ),

        # -----------------------------------
        # PRODUCT INFO
        # -----------------------------------

        "product": {

            "name": extracted_data.get(
                "product_name"
            ),

            "brand": extracted_data.get(
                "brand_name"
            ),

            "category": extracted_data.get(
                "product_category"
            ),

            "document_type": extracted_data.get(
                "document_type"
            ),
        },

        # -----------------------------------
        # SCORES
        # -----------------------------------

        "scores": score_data.get(
            "scores",
            {}
        ),

        # -----------------------------------
        # INGREDIENT STATS
        # -----------------------------------

        "ingredient_stats": score_data.get(
            "ingredient_stats",
            {}
        ),

        # -----------------------------------
        # EXPOSURE BREAKDOWN
        # -----------------------------------

        "exposure": score_data.get(
            "exposure",
            {}
        ),

        # -----------------------------------
        # POSITIVE HIGHLIGHTS
        # -----------------------------------

        "highlights": score_data.get(
            "highlights",
            []
        ),

        # -----------------------------------
        # FINDINGS
        # -----------------------------------

        "findings": score_data.get(
            "findings",
            []
        ),

        # -----------------------------------
        # WARNINGS
        # -----------------------------------

        "warnings": score_data.get(
            "warnings",
            []
        ),

        # -----------------------------------
        # NUTRITION
        # -----------------------------------

        "nutrition": score_data.get(
            "nutrition",
            {}
        ),

        # -----------------------------------
        # RAW EXTRACTION DATA
        # -----------------------------------

        "ingredients": extracted_data.get(
            "ingredients",
            []
        ),

        "claims": extracted_data.get(
            "claims",
            []
        ),

        "allergens": extracted_data.get(
            "allergens",
            []
        ),

        # -----------------------------------
        # META
        # -----------------------------------

        "meta": {

            "filename": filename,

            "ocr_quality": extracted_data.get(
                "ocr_quality"
            ),

            "ingredient_count": len(
                extracted_data.get(
                    "ingredients",
                    []
                )
            ),

            "ingredients_detected":
                extracted_data.get(
                    "has_ingredient_list",
                    False
                ),

            "nutrition_detected":
                extracted_data.get(
                    "has_nutrition_table",
                    False
                ),

            "findings_detected":
                len(
                    score_data.get(
                        "findings",
                        []
                    )
                ) > 0,
        }
    }

    # -----------------------------------
    # Final Cleanup
    # -----------------------------------

    return remove_empty(response)