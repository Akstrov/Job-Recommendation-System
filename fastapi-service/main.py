from fastapi import FastAPI, status

app = FastAPI(
    title="FastAPI Service",
    description="Basic API structure with health check endpoint",
    version="0.1.0",
)


@app.get("/")
def read_root():
    """Root endpoint that returns a welcome message"""
    return {"message": "Welcome to FastAPI Service"}


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """health check endpoint to verify the service is running"""
    return {"status": "healthy", "service": "fastapi_service", "version": "0.1.0"}
