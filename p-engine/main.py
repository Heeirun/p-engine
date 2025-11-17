"""P-Engine FastAPI Application.

A production-ready search engine with semantic and hybrid search capabilities.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controllers import items_router, search_router
from .dependencies import DependencyContainer


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler for startup and shutdown events.

    Initializes shared resources on startup and cleans up on shutdown.
    """
    # Startup: Initialize dependencies
    DependencyContainer.get_elasticsearch()
    DependencyContainer.get_embedding_model()
    yield
    # Shutdown: Clean up resources
    DependencyContainer.close()


# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Search engine with semantic and hybrid search capabilities",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items_router)
app.include_router(search_router)


@app.get("/", tags=["health"])
def read_root():
    """
    Health check endpoint.

    Returns:
        Dictionary with a welcome message
    """
    return {"message": f"Welcome to {settings.app_name}", "status": "healthy"}
