from typing import Dict
from collections import defaultdict


def calculate_scores(scan_data: Dict):

    ingredients = scan_data.get("ingredients", [])
    nutrition = scan_data.get("nutrition")
    claims = scan_data.get("claims", [])

    # -----------------------------------
    # Base Scores
    # -----------------------------------

    toxicity_score = 5
    hormonal_risk_score = 0
    nutrition_risk_score = 0
    processed_score = 0

    findings_map = defaultdict(list)

    claim_warnings = []
    positive_highlights = []

    natural_count = 0
    synthetic_count = 0

    edc_count = 0
    preservative_count = 0
    fragrance_count = 0

    # -----------------------------------
    # Risk Weights
    # -----------------------------------

    edc_penalties = {
        "Paraben": 18,
        "Phthalate": 25,
        "PFAS": 35,
        "BPA": 35,
        "Heavy Metal": 40,
        "Fragrance": 12,
    }

    risk_tag_penalties = {
        "irritant": 4,
        "allergen": 3,
        "formaldehyde releaser": 12,
        "carcinogenic": 30,
        "endocrine disruptor": 25,
        "neurotoxic": 25,
    }

    artificial_types = {
        "Preservative",
        "Artificial Color",
        "Sweetener",
        "Fragrance",
        "Surfactant",
    }

    # -----------------------------------
    # Ingredient Analysis
    # -----------------------------------

    for ingredient in ingredients:

        ingredient_name = ingredient.get(
            "normalized_name",
            "Unknown Ingredient"
        )

        ingredient_type = ingredient.get(
            "ingredient_type",
            "Unknown"
        )

        risk_tags = ingredient.get(
            "risk_tags",
            []
        )

        detected_edc = ingredient.get(
            "detected_edc",
            False
        )

        is_natural = ingredient.get(
            "is_natural"
        )

        ingredient_toxicity = 0
        ingredient_hormonal = 0

        # -----------------------------
        # Natural / Synthetic Counts
        # -----------------------------

        if is_natural is True:
            natural_count += 1

        elif is_natural is False:
            synthetic_count += 1

        # -----------------------------
        # Ingredient Counters
        # -----------------------------

        if ingredient_type == "Preservative":
            preservative_count += 1

        if ingredient_type == "Fragrance":
            fragrance_count += 1

        # -----------------------------
        # EDC Detection
        # -----------------------------

        if detected_edc:

            edc_count += 1

            ingredient_hormonal += 15
            ingredient_toxicity += 10

            findings_map[ingredient_name].append(
                "Potential endocrine disruptor"
            )

        # -----------------------------
        # Ingredient Type Penalties
        # -----------------------------

        if ingredient_type in edc_penalties:

            penalty = edc_penalties[ingredient_type]

            ingredient_hormonal += penalty
            ingredient_toxicity += penalty * 0.8

        # -----------------------------
        # Risk Tags
        # -----------------------------

        for tag in risk_tags:

            if tag in risk_tag_penalties:

                penalty = risk_tag_penalties[tag]

                ingredient_toxicity += penalty

                findings_map[ingredient_name].append(
                    tag
                )

        # -----------------------------
        # Ingredient Caps
        # -----------------------------

        ingredient_toxicity = min(
            ingredient_toxicity,
            25
        )

        ingredient_hormonal = min(
            ingredient_hormonal,
            30
        )

        toxicity_score += ingredient_toxicity
        hormonal_risk_score += ingredient_hormonal

        # -----------------------------
        # Processed Product Score
        # -----------------------------

        if ingredient_type in artificial_types:
            processed_score += 6

    # -----------------------------------
    # Nutrition Analysis
    # -----------------------------------

    if nutrition:

        sugar = nutrition.get("sugar")
        sodium = nutrition.get("sodium")
        trans_fat = nutrition.get("trans_fat")
        added_sugar = nutrition.get("added_sugar")

        # Sugar

        if sugar and sugar.get("value"):

            sugar_value = sugar["value"]

            if sugar_value >= 25:
                nutrition_risk_score += 20

            elif sugar_value >= 15:
                nutrition_risk_score += 10

        # Added Sugar

        if added_sugar and added_sugar.get("value"):

            added_sugar_value = added_sugar["value"]

            if added_sugar_value >= 20:
                nutrition_risk_score += 20

            elif added_sugar_value >= 10:
                nutrition_risk_score += 10

        # Sodium

        if sodium and sodium.get("value"):

            sodium_value = sodium["value"]

            if sodium_value >= 600:
                nutrition_risk_score += 15

            elif sodium_value >= 300:
                nutrition_risk_score += 8

        # Trans Fat

        if trans_fat and trans_fat.get("value"):

            trans_fat_value = trans_fat["value"]

            if trans_fat_value > 0:
                nutrition_risk_score += 20

    # -----------------------------------
    # Score Normalization
    # -----------------------------------

    toxicity_score = min(
        round(toxicity_score),
        100
    )

    hormonal_risk_score = min(
        round(hormonal_risk_score),
        100
    )

    nutrition_risk_score = min(
        round(nutrition_risk_score),
        100
    )

    processed_score = min(
        round(processed_score),
        100
    )

    # -----------------------------------
    # Clean Beauty Score
    # -----------------------------------

    total_ingredients = max(
        len(ingredients),
        1
    )

    natural_ratio = (
        natural_count / total_ingredients
    )

    synthetic_ratio = (
        synthetic_count / total_ingredients
    )

    clean_beauty_score = round(
        (
            natural_ratio * 100
        )
        - (
            synthetic_ratio * 20
        )
        - (
            toxicity_score * 0.2
        )
    )

    clean_beauty_score = max(
        min(clean_beauty_score, 100),
        0
    )

    # -----------------------------------
    # Overall Health Score
    # -----------------------------------

    overall_health_score = round(
        (
            (100 - toxicity_score) * 0.35
            + (100 - hormonal_risk_score) * 0.30
            + (100 - nutrition_risk_score) * 0.15
            + clean_beauty_score * 0.20
        )
    )

    overall_health_score = max(
        min(overall_health_score, 95),
        0
    )

    # -----------------------------------
    # Claims Validation
    # -----------------------------------

    claims_text = " ".join(
        claims
    ).lower()

    if "paraben free" in claims_text:

        for ingredient in ingredients:

            if ingredient.get(
                "ingredient_type"
            ) == "Paraben":

                claim_warnings.append(
                    "Product claims paraben-free but parabens may be present"
                )

    if "sulphate free" in claims_text:

        for ingredient in ingredients:

            if ingredient.get(
                "ingredient_type"
            ) == "Surfactant":

                claim_warnings.append(
                    "Product claims sulphate-free but surfactants detected"
                )

    # -----------------------------------
    # Positive Highlights
    # -----------------------------------

    if edc_count == 0:
        positive_highlights.append(
            "No major endocrine disruptors detected"
        )

    if natural_count > synthetic_count:
        positive_highlights.append(
            "Contains mostly natural ingredients"
        )

    if fragrance_count == 0:
        positive_highlights.append(
            "No synthetic fragrance detected"
        )

    if preservative_count <= 1:
        positive_highlights.append(
            "Low preservative load"
        )

    if processed_score <= 20:
        positive_highlights.append(
            "Low synthetic additive load"
        )

    if toxicity_score <= 20:
        positive_highlights.append(
            "Low overall toxicity risk"
        )

    # -----------------------------------
    # Safe Empty States
    # -----------------------------------

    if not ingredients:

        positive_highlights.append(
            "No ingredient list detected"
        )

    if not findings_map and ingredients:

        positive_highlights.append(
            "No major concerns detected"
        )

    # -----------------------------------
    # Remove Duplicates
    # -----------------------------------

    positive_highlights = list(
        dict.fromkeys(positive_highlights)
    )

    claim_warnings = list(
        dict.fromkeys(claim_warnings)
    )

    # -----------------------------------
    # Risk Classification
    # -----------------------------------

    def classify(score):

        if score >= 70:
            return "HIGH"

        elif score >= 40:
            return "MODERATE"

        return "LOW"

    # -----------------------------------
    # Group Findings
    # -----------------------------------

    findings = []

    for ingredient, issues in findings_map.items():

        findings.append({
            "ingredient": ingredient,
            "issues": list(set(issues))
        })

    # -----------------------------------
    # Exposure Breakdown
    # -----------------------------------

    exposure_breakdown = {
        "endocrine_disruptors":
            edc_count,

        "preservatives":
            preservative_count,

        "synthetic_ingredients":
            synthetic_count,

        "natural_ingredients":
            natural_count,

        "fragrances":
            fragrance_count
    }

    # -----------------------------------
    # Final Response
    # -----------------------------------

    return {

        "scan_status": "completed",

        "meta": {

            "has_ingredients":
                len(ingredients) > 0,

            "has_nutrition":
                nutrition is not None,

            "has_findings":
                len(findings) > 0,

            "has_claim_warnings":
                len(claim_warnings) > 0,

            "total_ingredients":
                len(ingredients)
        },

        "overall_health_score":
            overall_health_score or 0,

        "scores": {

            "toxicity": {
                "score":
                    toxicity_score or 0,

                "level":
                    classify(toxicity_score)
            },

            "hormonal": {
                "score":
                    hormonal_risk_score or 0,

                "level":
                    classify(hormonal_risk_score)
            },

            "nutrition": {
                "score":
                    nutrition_risk_score or 0,

                "level":
                    classify(nutrition_risk_score)
            },

            "processed": {
                "score":
                    processed_score or 0
            },

            "clean_beauty": {
                "score":
                    clean_beauty_score or 0
            }
        },

        "ingredient_summary": {

            "natural_count":
                natural_count or 0,

            "synthetic_count":
                synthetic_count or 0,

            "preservative_count":
                preservative_count or 0,

            "edc_count":
                edc_count or 0,

            "fragrance_count":
                fragrance_count or 0
        },

        "positive_highlights":
            positive_highlights or [],

        "findings":
            findings or [],

        "claim_warnings":
            claim_warnings or [],

        "exposure_breakdown":
            exposure_breakdown or {},

        "nutrition":
            nutrition or {},

        "ui": {

            "primary_score":
                overall_health_score or 0,

            "primary_label": (
                "Excellent"
                if overall_health_score >= 85 else
                "Good"
                if overall_health_score >= 70 else
                "Moderate"
                if overall_health_score >= 50 else
                "High Risk"
            ),

            "risk_color": (
                "green"
                if toxicity_score < 30 else
                "yellow"
                if toxicity_score < 60 else
                "red"
            ),

            "score_ring_color": (
                "emerald"
                if overall_health_score >= 80 else
                "yellow"
                if overall_health_score >= 50 else
                "red"
            )
        }
    }