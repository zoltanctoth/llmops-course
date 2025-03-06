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
    print("Loading model...")
    mlflow_model = mlflow.pyfunc.load_model("./article_summarizer")
    print("Model loaded")
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
