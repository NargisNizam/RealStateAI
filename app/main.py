from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.recommender import recommend_properties
from app.ai_assistant import ask_real_estate_assistant
from app.rag import ask_rag_assistant


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="RealEstateAI",
    description="AI Real Estate Intelligence Platform",
    version="1.0.0"
)


# --------------------------------------------------
# Static Files & Templates
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )

# --------------------------------------------------
# AI Assistant API
# --------------------------------------------------

@app.post("/api/ai-assistant")
async def ai_assistant(question: str = Form(...)):

    try:

        answer = ask_real_estate_assistant(
            question
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# --------------------------------------------------
# RAG Assistant API
# --------------------------------------------------

@app.post("/api/rag")
async def rag_assistant(question: str = Form(...)):

    try:

        result = ask_rag_assistant(
            question
        )

        return {
            "success": True,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# --------------------------------------------------
# Property Recommendation API
# --------------------------------------------------

@app.post("/api/recommend")
async def recommend(
    budget: float = Form(...),
    city: str = Form(""),
    bedrooms: int = Form(0),
    property_type: str = Form("")
):

    try:

        recommendations = recommend_properties(
            budget=budget,
            city=city if city else None,
            bedrooms=bedrooms if bedrooms > 0 else None,
            property_type=property_type if property_type else None,
            top_n=5
        )

        return {
            "success": True,
            "recommendations": recommendations
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "project": "RealEstateAI"
    }