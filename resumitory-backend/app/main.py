from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.resumes.router import router as resumes_router
from app.applications.router import router as applications_router

app = FastAPI(
    title="Resumitory API",
    description="Resume version control and job application tracker",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(resumes_router, prefix="/resumes", tags=["Resumes"])
app.include_router(applications_router, prefix="/applications", tags=["Applications"])
# TODO: Add rounds router (V1.1)


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Resumitory API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
