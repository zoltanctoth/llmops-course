# syntax=docker/dockerfile:1
# check=skip=SecretsUsedInArgOrEnv
FROM python:3.12-slim

# Environment variable for Gemini API key (will be passed at runtime)
ENV GEMINI_API_KEY=""

RUN mkdir -p /app/
WORKDIR /app

COPY model ./model
RUN pip install -r model/requirements.txt

# Copy the FastAPI application
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY model_serving.py .

# Expose the port
EXPOSE 8421

# Run the FastAPI application with Gunicorn
CMD ["python", "model_serving.py"]
