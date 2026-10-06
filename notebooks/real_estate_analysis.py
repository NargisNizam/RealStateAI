import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# LOAD CLEANED DATA
# ==========================================

file_path = "data/processed/cleaned_properties.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# BASIC INFORMATION
# ==========================================

print("\n========== DATA INFO ==========")
print(df.info())

print("\n========== STATISTICS ==========")
print(df.describe())


# ==========================================
# 1. PROPERTY PRICE DISTRIBUTION
# ==========================================

plt.figure(figsize=(10, 6))

sns.histplot(
    df["price_pkr"],
    bins=50,
    kde=True
)

plt.title("Property Price Distribution")
plt.xlabel("Price (PKR)")
plt.ylabel("Number of Properties")

plt.tight_layout()
plt.show()


# ==========================================
# 2. PROPERTY TYPES
# ==========================================

property_types = df["type"].value_counts()

print("\n========== PROPERTY TYPES ==========")
print(property_types)

plt.figure(figsize=(10, 6))

property_types.plot(kind="bar")

plt.title("Property Types")
plt.xlabel("Property Type")
plt.ylabel("Number of Properties")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ==========================================
# 3. TOP CITIES
# ==========================================

top_cities = df["location_city"].value_counts().head(10)

print("\n========== TOP 10 CITIES ==========")
print(top_cities)

plt.figure(figsize=(10, 6))

top_cities.plot(kind="bar")

plt.title("Top 10 Cities by Number of Properties")
plt.xlabel("City")
plt.ylabel("Number of Properties")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ==========================================
# 4. AREA VS PRICE
# ==========================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df.sample(min(5000, len(df)), random_state=42),
    x="area_marla",
    y="price_pkr",
    alpha=0.5
)

plt.title("Area vs Property Price")
plt.xlabel("Area (Marla)")
plt.ylabel("Price (PKR)")

plt.tight_layout()
plt.show()


# ==========================================
# 5. BEDROOMS VS PRICE
# ==========================================

bedroom_price = (
    df.groupby("bedroom")["price_pkr"]
    .mean()
    .sort_index()
)

print("\n========== AVERAGE PRICE BY BEDROOMS ==========")
print(bedroom_price)

plt.figure(figsize=(10, 6))

bedroom_price.plot(kind="bar")

plt.title("Average Property Price by Number of Bedrooms")
plt.xlabel("Bedrooms")
plt.ylabel("Average Price (PKR)")

plt.tight_layout()
plt.show()


# ==========================================
# 6. BATHROOMS VS PRICE
# ==========================================

bath_price = (
    df.groupby("bath")["price_pkr"]
    .mean()
    .sort_index()
)

print("\n========== AVERAGE PRICE BY BATHROOMS ==========")
print(bath_price)

plt.figure(figsize=(10, 6))

bath_price.plot(kind="bar")

plt.title("Average Property Price by Number of Bathrooms")
plt.xlabel("Bathrooms")
plt.ylabel("Average Price (PKR)")

plt.tight_layout()
plt.show()


# ==========================================
# 7. AVERAGE PRICE BY CITY
# ==========================================

city_price = (
    df.groupby("location_city")["price_pkr"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 CITIES BY AVERAGE PRICE ==========")
print(city_price)

plt.figure(figsize=(10, 6))

city_price.plot(kind="bar")

plt.title("Top 10 Cities by Average Property Price")
plt.xlabel("City")
plt.ylabel("Average Price (PKR)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ==========================================
# 8. CORRELATION ANALYSIS
# ==========================================

numeric_columns = [
    "bedroom",
    "bath",
    "price_pkr",
    "area_marla",
    "price_per_marla"
]

correlation = df[numeric_columns].corr()

print("\n========== CORRELATION MATRIX ==========")
print(correlation)

plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Real Estate Feature Correlation")

plt.tight_layout()
plt.show()


# ==========================================
# EDA COMPLETED
# ==========================================

print("\n==========================================")
print("EDA AND VISUALIZATION COMPLETED")
print("==========================================")