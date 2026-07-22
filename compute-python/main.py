from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Lead Hunter Compute Engine",
    description="Python FastAPI backend for data processing, Pandas/NumPy operations, and AI compute tasks.",
    version="1.0.0"
)

# Configure CORS to allow seamless communication from the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local Docker development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    """Root endpoint to verify the service is running."""
    return {"message": "Compute Engine API is online and listening!"}

@app.get("/health")
def health_check():
    """Health check endpoint for Docker container status."""
    return {"status": "healthy", "service": "compute-engine"}

@app.post("/api/v1/analyze")
def analyze_data(payload: dict):
    """
    Placeholder endpoint for future data processing.
    This is where Pandas and NumPy logic will live.
    """
    return {
        "status": "success",
        "message": "Data analyzed successfully",
        "processed_keys": list(payload.keys())
    }

if __name__ == "__main__":
    # Binding to 0.0.0.0 is CRITICAL for Docker so the port is exposed outside the container
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
