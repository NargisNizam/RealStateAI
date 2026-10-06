import pandas as pd


# ==========================================
# LOAD PROPERTY DATA
# ==========================================

DATA_FILE = "data/processed/cleaned_properties.csv"

df = pd.read_csv(DATA_FILE)


# ==========================================
# REMOVE EXTREME VALUES
# ==========================================

df = df[
    (df["bedroom"] >= 1) &
    (df["bedroom"] <= 12) &
    (df["bath"] >= 1) &
    (df["bath"] <= 12) &
    (df["price_pkr"] >= 100_000)
].copy()


# ==========================================
# RECOMMEND PROPERTIES
# ==========================================

def recommend_properties(
    budget,
    city=None,
    bedrooms=None,
    property_type=None,
    purpose="For Sale",
    top_n=5
):

    recommendations = df.copy()

    # --------------------------------------
    # PURPOSE FILTER
    # --------------------------------------

    if purpose:
        recommendations = recommendations[
            recommendations["purpose"].str.lower()
            == purpose.lower()
        ]

    # --------------------------------------
    # CITY FILTER
    # --------------------------------------

    if city:
        city_mask = (
            recommendations["location_city"]
            .str.lower()
            .str.contains(city.lower(), na=False)
        )

        recommendations = recommendations[city_mask]

    # --------------------------------------
    # BEDROOM FILTER
    # --------------------------------------

    if bedrooms:
        recommendations["bedroom_difference"] = (
            recommendations["bedroom"] - bedrooms
        ).abs()

    else:
        recommendations["bedroom_difference"] = 0

    # --------------------------------------
    # BUDGET FILTER
    # --------------------------------------

    # Prefer properties within budget
    within_budget = recommendations[
        recommendations["price_pkr"] <= budget
    ].copy()

    # If no property is within budget,
    # find properties slightly above budget
    if len(within_budget) > 0:

        recommendations = within_budget

    else:

        recommendations["budget_difference"] = (
            recommendations["price_pkr"] - budget
        ).abs()

        recommendations = recommendations.sort_values(
            "budget_difference"
        ).head(50)

    # --------------------------------------
    # PROPERTY TYPE
    # --------------------------------------

    if property_type:

        type_mask = (
            recommendations["type"]
            .str.lower()
            .str.contains(property_type.lower(), na=False)
        )

        type_matches = recommendations[type_mask].copy()

        if len(type_matches) > 0:
            recommendations = type_matches

    # --------------------------------------
    # SCORE
    # --------------------------------------

    recommendations["budget_difference"] = (
        recommendations["price_pkr"] - budget
    ).abs()

    recommendations["bedroom_difference"] = (
        recommendations["bedroom"] - bedrooms
    ).abs() if bedrooms else 0

    # Normalize differences
    recommendations["budget_score"] = (
        recommendations["budget_difference"] /
        max(budget, 1)
    )

    recommendations["bedroom_score"] = (
        recommendations["bedroom_difference"] /
        max(bedrooms, 1)
    ) if bedrooms else 0

    # Combined score
    recommendations["score"] = (
        recommendations["budget_score"] * 0.6
        +
        recommendations["bedroom_score"] * 0.4
    )

    # --------------------------------------
    # SORT
    # --------------------------------------

    recommendations = recommendations.sort_values(
        "score"
    )

    recommendations = recommendations.head(top_n)


    # ======================================
    # CREATE EXPLANATION
    # ======================================

    results = []

    for _, row in recommendations.iterrows():

        reasons = []

        if row["price_pkr"] <= budget:
            reasons.append("within your budget")

        if bedrooms:
            if row["bedroom"] == bedrooms:
                reasons.append(
                    f"{int(row['bedroom'])} bedrooms match your requirement"
                )
            elif abs(row["bedroom"] - bedrooms) <= 1:
                reasons.append(
                    "bedroom count is close to your requirement"
                )

        if city:
            reasons.append(
                f"located in {row['location_city']}"
            )

        results.append({
            "type": row["type"],
            "city": row["location_city"],
            "location": row["location"],
            "bedrooms": int(row["bedroom"]),
            "bathrooms": int(row["bath"]),
            "area_marla": round(row["area_marla"], 2),
            "price_pkr": row["price_pkr"],
            "price_per_marla": row["price_per_marla"],
            "reason": ", ".join(reasons)
        })

    return results
    groq