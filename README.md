# 🏠 RealEstateAI — AI Real Estate Intelligence Platform

RealEstateAI is an AI-powered real estate intelligence platform that combines **Data Analysis, Machine Learning, Property Recommendation, Generative AI, and RAG (Retrieval-Augmented Generation)** into one web application.

The platform helps users analyze property data, estimate property prices, find suitable properties based on their preferences, and ask real estate-related questions using AI.

---

## 🚀 Features

### 📊 1. Real Estate Data Analysis

The project analyzes a real estate dataset using:

- Pandas
- NumPy
- Matplotlib
- Seaborn

Analysis includes:

- Property price distribution
- Property type analysis
- Location comparison
- Area vs. price analysis
- Bedrooms vs. price
- Bathrooms vs. price
- City-wise average prices
- Correlation analysis

---

### 🤖 2. Machine Learning Price Prediction

A Machine Learning model is trained to predict property prices based on:

- Property Type
- Purpose
- Bedrooms
- Bathrooms
- City
- Province
- Area in Marla

The project uses a **Random Forest Regressor** with preprocessing and One-Hot Encoding.

### Model Performance

- **R² Score:** 0.7092
- **MAE:** PKR 12,027,889
- **RMSE:** PKR 37,441,009

The trained model is saved as:

```text
models/price_model.pkl
🏡 3. Property Recommendation System

The recommendation system finds properties according to user preferences such as:

Budget
Location
Bedrooms
Property Type
Purpose

The system ranks suitable properties and provides a reason for each recommendation.

Example:

Budget: PKR 20,000,000
Location: Lahore
Bedrooms: 4
Property Type: House
The system returns matching properties within or close to the user's budget.

💬 4. AI Real Estate Assistant

RealEstateAI includes a Generative AI assistant powered by Groq.

The AI assistant can answer questions about:

Property buying
Real estate prices
Location factors
Investment considerations
Property selection
Real estate terminology
General buying guidance

The assistant uses prompt engineering to provide relevant and responsible responses.

📚 5. RAG Knowledge Assistant

The project also includes a Retrieval-Augmented Generation (RAG) system.

Users can ask questions about information stored in real estate documents.

Knowledge sources include:

Property Buying Guide
Real Estate Investment Tips
Property Documentation Guide

The RAG pipeline uses:

Documents
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Sentence Transformers
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Relevant Document Retrieval
    ↓
Groq LLM
    ↓
AI Answer

The RAG assistant provides the sources used to generate the answer.

🌐 6. FastAPI Web Interface

The entire project is integrated into a FastAPI web application.

The web interface provides:

🏠 RealEstateAI Dashboard
💰 Price Prediction
🏡 Property Recommendations
🤖 AI Real Estate Assistant
📚 RAG Knowledge Assistant
🛠️ Technologies Used
Programming
Python
Data Science
Pandas
NumPy
Matplotlib
Seaborn
Machine Learning
Scikit-learn
Random Forest Regressor
One-Hot Encoding
Pipeline
Generative AI
Groq API
LLM
Prompt Engineering
RAG
ChromaDB
Sentence Transformers
PyPDF
Backend
FastAPI
Uvicorn
Jinja2
Frontend
HTML
CSS
JavaScript
Model Storage
Joblib
📁 Project Structure
RealEstateAI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── ml_model.py
│   ├── recommender.py
│   ├── rag.py
│   └── ai_assistant.py
│
├── data/
│   ├── raw/
│   │   └── raw_data_zameen.csv
│   │
│   └── processed/
│       └── cleaned_properties.csv
│
├── models/
│   └── price_model.pkl
│
├── notebooks/
│   └── real_estate_analysis.py
│
├── rag_documents/
│   ├── property_buying_guide.txt
│   ├── real_estate_investment_tips.txt
│   └── property_documentation_guide.txt
│
├── scripts/
│   ├── data_cleaning.py
│   ├── train_model.py
│   ├── test_recommender.py
│   ├── test_ai_assistant.py
│   └── ingest_documents.py
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── report/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
⚙️ Installation
1. Clone the Repository
git clone https://github.com/NargisNizam/RealStateAI.git
2. Open the Project
cd RealStateAI
3. Create Virtual Environment
python -m venv venv
4. Activate Virtual Environment

Windows:

venv\Scripts\activate
5. Install Dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

Never upload your real API key to GitHub.

The .env file should be included in .gitignore.

📊 Data Processing

Run the data cleaning script:

python scripts\data_cleaning.py

This processes the raw Zameen dataset and creates:

data/processed/cleaned_properties.csv
🤖 Train the ML Model

Run:

python scripts\train_model.py

The trained model will be saved as:

models/price_model.pkl
🏡 Test Recommendation System

Run:

python scripts\test_recommender.py
💬 Test AI Assistant

Run:

python scripts\test_ai_assistant.py
📚 Build RAG Knowledge Base

Run:

python scripts\ingest_documents.py

This processes the documents and stores their embeddings in ChromaDB.

🌐 Run the Web Application

Start FastAPI:

uvicorn app.main:app --reload

Open the application in your browser:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs
🧠 RAG Architecture
Real Estate Documents
        │
        ▼
   Text Extraction
        │
        ▼
    Text Chunking
        │
        ▼
 Sentence Transformer
        │
        ▼
    Embeddings
        │
        ▼
     ChromaDB
        │
        ▼
 Relevant Documents
        │
        ▼
      Groq LLM
        │
        ▼
    Final Answer
📈 Machine Learning Workflow
Raw Dataset
     │
     ▼
Data Cleaning
     │
     ▼
Preprocessing
     │
     ▼
Feature Selection
     │
     ▼
Train/Test Split
     │
     ▼
Random Forest Model
     │
     ▼
Model Evaluation
     │
     ▼
price_model.pkl
     │
     ▼
FastAPI Prediction API
🎯 Project Objectives

The main objectives of RealEstateAI are:

Analyze real estate market data.
Predict property prices using Machine Learning.
Recommend properties according to user preferences.
Provide an AI-powered real estate assistant.
Build a RAG-based knowledge assistant.
Integrate all components into a FastAPI web application.
Provide a clean and user-friendly interface.
🔮 Future Improvements

Future versions can include:

Live property listings
Interactive maps
More advanced price prediction models
XGBoost/LightGBM comparison
User authentication
Property comparison
Favorite properties
Market trend forecasting
Real-time property APIs
Multilingual AI assistant
Voice-based real estate assistant
⚠️ Disclaimer

RealEstateAI is an educational and demonstration project.

Price predictions, recommendations, and AI responses should not be considered professional financial, legal, or real estate advice.

Users should independently verify property information and consult qualified professionals before making real estate decisions.

👩‍💻 Author

Nargis Nizam

AI & Data Science Student | Data Analyst | Web Developer

GitHub:
https://github.com/NargisNizam

⭐ Acknowledgement

This project was developed as an AI and Data Science project combining:

Data Science + Machine Learning + Generative AI + RAG + FastAPI


### Ab README save karne ke baad

PowerShell mein:

```powershell
git add README.md
git commit -m "Add project README"
git push -u origin main

Agar src refspec main does not match any wala error dobara aaye, to pehle:

git branch -M main
git add .
git commit -m "Initial commit - RealEstateAI"
git push -u origin main
