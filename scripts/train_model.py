import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# LOAD DATA
# ==========================================

input_file = "data/processed/cleaned_properties.csv"

df = pd.read_csv(input_file)

print("\n========== DATA LOADED ==========")
print("Shape:", df.shape)


# ==========================================
# REMOVE EXTREME / INVALID OUTLIERS
# ==========================================

print("\n========== BEFORE OUTLIER CLEANING ==========")
print("Rows:", len(df))

# Keep realistic bedroom values
df = df[
    (df["bedroom"] >= 1) &
    (df["bedroom"] <= 12)
]

# Keep realistic bathroom values
df = df[
    (df["bath"] >= 1) &
    (df["bath"] <= 12)
]

# Remove extremely low prices
df = df[df["price_pkr"] >= 100_000]

# Keep realistic area range
df = df[
    (df["area_marla"] >= 1) &
    (df["area_marla"] <= 100)
]

print("\n========== AFTER OUTLIER CLEANING ==========")
print("Rows:", len(df))
print("Removed:", 43221 - len(df))


# ==========================================
# FEATURES AND TARGET
# ==========================================

features = [
    "type",
    "purpose",
    "bedroom",
    "bath",
    "location_city",
    "location_province",
    "area_marla"
]

target = "price_pkr"

X = df[features]
y = df[target]


print("\n========== FEATURES ==========")
print(features)

print("\nTarget:", target)


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\n========== DATA SPLIT ==========")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# CATEGORICAL FEATURES
# ==========================================

categorical_features = [
    "type",
    "purpose",
    "location_city",
    "location_province"
]

numeric_features = [
    "bedroom",
    "bath",
    "area_marla"
]


# ==========================================
# PREPROCESSING
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# ==========================================
# RANDOM FOREST MODEL
# ==========================================

model = RandomForestRegressor(
    n_estimators=150,
    random_state=42,
    n_jobs=-1,
    max_depth=20
)


# ==========================================
# PIPELINE
# ==========================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ==========================================
# TRAIN MODEL
# ==========================================

print("\n========== TRAINING MODEL ==========")

pipeline.fit(X_train, y_train)

print("Model training completed!")


# ==========================================
# PREDICTIONS
# ==========================================

y_pred = pipeline.predict(X_test)


# ==========================================
# EVALUATION
# ==========================================

mae = mean_absolute_error(y_test, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_test, y_pred)
)

r2 = r2_score(y_test, y_pred)


print("\n========== MODEL EVALUATION ==========")

print(f"MAE  : PKR {mae:,.2f}")
print(f"RMSE : PKR {rmse:,.2f}")
print(f"R²   : {r2:.4f}")


# ==========================================
# SAMPLE PREDICTIONS
# ==========================================

results = pd.DataFrame({
    "Actual Price": y_test.values[:10],
    "Predicted Price": y_pred[:10]
})

print("\n========== SAMPLE PREDICTIONS ==========")
print(results)


# ==========================================
# SAVE MODEL
# ==========================================

os.makedirs("models", exist_ok=True)

model_file = "models/price_model.pkl"

joblib.dump(
    pipeline,
    model_file
)

print("\n==========================================")
print("MODEL TRAINING COMPLETED SUCCESSFULLY")
print("==========================================")

print("\nModel saved at:")
print(model_file)