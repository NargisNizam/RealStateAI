import pandas as pd
import numpy as np
import os
import re

# ==========================================
# 1. Load Dataset
# ==========================================

input_file = "data/raw/raw_data_zameen.csv"

df = pd.read_csv(input_file)

print("\n========== ORIGINAL DATASET ==========")
print("Shape:", df.shape)

# ==========================================
# 2. Clean Column Names
# ==========================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\n========== COLUMNS ==========")
print(df.columns.tolist())

# ==========================================
# 3. Remove Duplicate Rows
# ==========================================

before = len(df)

df = df.drop_duplicates()

after = len(df)

print("\n========== DUPLICATES ==========")
print("Removed:", before - after)

# ==========================================
# 4. Clean Price
# ==========================================

def convert_price(value):

    if pd.isna(value):
        return np.nan

    value = str(value)

    # Remove PKR and newline
    value = value.replace("PKR", "")
    value = value.replace("\\n", "")
    value = value.replace("\n", "")
    value = value.strip()

    # Extract number
    match = re.search(r"([\d.]+)", value)

    if not match:
        return np.nan

    number = float(match.group(1))

    value_lower = value.lower()

    if "crore" in value_lower:
        return number * 10_000_000

    elif "lakh" in value_lower:
        return number * 100_000

    elif "million" in value_lower:
        return number * 1_000_000

    else:
        return number


df["price_pkr"] = df["price"].apply(convert_price)

# ==========================================
# 5. Clean Area
# ==========================================

def convert_area_to_marla(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip().lower()

    match = re.search(r"([\d.]+)", value)

    if not match:
        return np.nan

    number = float(match.group(1))

    # 1 Kanal = 20 Marla
    if "kanal" in value:
        return number * 20

    elif "marla" in value:
        return number

    else:
        return number


df["area_marla"] = df["area"].apply(convert_area_to_marla)

# ==========================================
# 6. Convert Bedrooms & Bathrooms
# ==========================================

df["bedroom"] = pd.to_numeric(
    df["bedroom"],
    errors="coerce"
)

df["bath"] = pd.to_numeric(
    df["bath"],
    errors="coerce"
)

# ==========================================
# 7. Missing Values
# ==========================================

print("\n========== MISSING VALUES BEFORE ==========")
print(df.isnull().sum())

# Price and area are essential for ML
df = df.dropna(
    subset=["price_pkr", "area_marla"]
)

# Fill bedrooms and bathrooms with median
df["bedroom"] = df["bedroom"].fillna(
    df["bedroom"].median()
)

df["bath"] = df["bath"].fillna(
    df["bath"].median()
)

# Location province
df["location_province"] = df[
    "location_province"
].fillna("Unknown")

# ==========================================
# 8. Remove Invalid Values
# ==========================================

df = df[df["price_pkr"] > 0]

df = df[df["area_marla"] > 0]

# ==========================================
# 9. Remove Extreme Unrealistic Values
# ==========================================

# Keep reasonable property areas
df = df[
    (df["area_marla"] >= 1) &
    (df["area_marla"] <= 100)
]

# Keep positive bedroom/bathroom values
df = df[df["bedroom"] >= 0]
df = df[df["bath"] >= 0]

# ==========================================
# 10. Create Price Per Marla
# ==========================================

df["price_per_marla"] = (
    df["price_pkr"] / df["area_marla"]
)

# ==========================================
# 11. Remove Unnecessary Columns
# ==========================================

columns_to_drop = [
    "index",
    "price",
    "area",
    "initial_amount",
    "monthly_installment",
    "remaining_installments"
]

for column in columns_to_drop:

    if column in df.columns:
        df = df.drop(columns=[column])

# ==========================================
# 12. Final Missing Values
# ==========================================

print("\n========== MISSING VALUES AFTER ==========")
print(df.isnull().sum())

# ==========================================
# 13. Final Dataset Information
# ==========================================

print("\n========== FINAL DATA TYPES ==========")
print(df.dtypes)

print("\n========== FINAL DATASET ==========")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# ==========================================
# 14. Display Important Statistics
# ==========================================

print("\n========== PRICE STATISTICS ==========")

print(
    df["price_pkr"].describe()
)

print("\n========== AREA STATISTICS ==========")

print(
    df["area_marla"].describe()
)

# ==========================================
# 15. Save Cleaned Dataset
# ==========================================

output_file = (
    "data/processed/cleaned_properties.csv"
)

os.makedirs(
    "data/processed",
    exist_ok=True
)

df.to_csv(
    output_file,
    index=False
)

# ==========================================
# 16. Final Output
# ==========================================

print("\n========================================")
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("========================================")

print("\nSaved file:")
print(output_file)

print("\nFinal shape:")
print(df.shape)

print("\nFinal columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())