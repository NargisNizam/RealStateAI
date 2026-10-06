import sys
import os

# Add project root to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app.recommender import recommend_properties


recommendations = recommend_properties(
    budget=20_000_000,
    city="Lahore",
    bedrooms=4,
    property_type="House",
    top_n=5
)


print("\n========== PROPERTY RECOMMENDATIONS ==========")

if not recommendations:
    print("No matching properties found.")

else:
    for i, property_data in enumerate(recommendations, start=1):

        print(f"\nProperty #{i}")

        print("Type:", property_data["type"])
        print("City:", property_data["city"])
        print("Location:", property_data["location"])
        print("Bedrooms:", property_data["bedrooms"])
        print("Bathrooms:", property_data["bathrooms"])
        print("Area:", property_data["area_marla"], "Marla")
        print(
            "Price:",
            f"PKR {property_data['price_pkr']:,.0f}"
        )
        print(
            "Price per Marla:",
            f"PKR {property_data['price_per_marla']:,.0f}"
        )
        print("Reason:", property_data["reason"])