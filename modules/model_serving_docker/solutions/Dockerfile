#FROM ghcr.io/mlflow/mlflow:v2.20.2
FROM python:3.12-slim

# Build argument for MLflow tracking URI
ARG AZURE_MLFLOW_TRACKING_URI
ENV AZURE_MLFLOW_TRACKING_URI=$AZURE_MLFLOW_TRACKING_URI

# Environment variable for Gemini API key (will be passed at runtime)
ENV GEMINI_API_KEY=""

RUN mkdir -p /app/
WORKDIR /app

# Copy the FastAPI application
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY model_serving.py .

# Copy and set up the model
#COPY model .

COPY download_model.py .
RUN pip install mlflow==2.20.3 azureml-mlflow
RUN python download_model.py

RUN pip install -r article_summarizer/requirements.txt

RUN mkdir -p modules/cloud_mlflow/
RUN cp -r article_summarizer/code/ modules/cloud_mlflow/

# Expose the port
EXPOSE 8000

# Run the FastAPI application with Gunicorn
CMD ["python", "model_serving.py"]
