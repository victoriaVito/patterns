from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from db.models import init_db
from api.routes_levels import router as levels_router
from api.routes_analysis import router as analysis_router

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Candy Crush Pattern Detection API",
    description="System for detecting and analyzing patterns in Candy Crush Soda Saga levels",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(levels_router)
app.include_router(analysis_router)

@app.get("/")
def read_root():
    return {
        "name": "Candy Crush Pattern Detection API",
        "version": "1.0.0",
        "endpoints": {
            "levels": "/docs#/levels",
            "analysis": "/docs#/analysis"
        },
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
