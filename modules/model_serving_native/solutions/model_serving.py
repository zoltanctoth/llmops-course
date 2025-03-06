import os
from pathlib import Path

import dotenv
import mlflow.pyfunc
import pandas as pd
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.post("/summarize")
async def summarize(article: dict[str, str]):
    """Endpoint to summarize article text."""

    df = pd.DataFrame([article])
    summary = mlflow_model.predict(df)[0]
    return {"summary": summary}


if __name__ == "__main__":
    # Use WORKSPACE_FOLDER environment variable to get the project root
    project_root = Path(os.getenv("WORKSPACE_FOLDER", "/workspaces/llmops-course"))
    dotenv.load_dotenv(project_root / ".env")

    mlflow.set_tracking_uri(os.getenv("AZURE_MLFLOW_TRACKING_URI"))
    mlflow_model = mlflow.pyfunc.load_model("models:/article_summarizer/9")

    # Run the FastAPI server
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
# Health check
curl http://localhost:8000/health

# Summarize
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "LLMOps is on the rise!"}'
"""
