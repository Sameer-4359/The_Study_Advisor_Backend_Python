# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import recommendations, universities

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="University Recommendation System API",
    description="Hybrid recommendation system for university admissions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations.router)
app.include_router(universities.router)

@app.get("/")
def root():
    return {
        "message": "University Recommendation System API",
        "version": "1.0.0",
        "endpoints": {
            "recommendations": "/recommendations",
            "universities": "/universities",
            "documentation": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "recommendation-system"}