import os
from pathlib import Path

import dotenv
import mlflow
from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository

project_root = Path(os.getenv("WORKSPACE_FOLDER", "/workspaces/llmops-course"))
dotenv.load_dotenv(project_root / ".env")

mlflow.set_tracking_uri("databricks")

# Get the latest production model
client = mlflow.tracking.MlflowClient()
model_versions = client.search_model_versions("name='article_summarizer'")
sorted_versions = sorted(model_versions, key=lambda x: int(x.version), reverse=True)

production_model = None
for version in sorted_versions:
    if "stage" in version.tags and version.tags["stage"] == "production":
        print(f"🎯 Production model found: {version.version}")
        print(f"📋 Production Model URI: models:/article_summarizer/{version.version}")
        break
else:
    raise Exception("No production model found")

MODEL_NAME = "article_summarizer"
model_uri = client.get_model_version_download_uri(MODEL_NAME, version.version)

MODEL_FOLDER = "model"
if os.path.exists(MODEL_FOLDER):
    print(f"🧹 Cleaning up existing {MODEL_FOLDER} folder")
    import shutil

    shutil.rmtree(MODEL_FOLDER)

print(f"📁 Creating {MODEL_FOLDER} folder")
os.makedirs(MODEL_FOLDER)

print(f"⬇️ Downloading model from {model_uri}")
# Download the model artifacts
repo = ModelsArtifactRepository(f"models:/{MODEL_NAME}/{version.version}")
repo.download_artifacts(artifact_path="", dst_path=MODEL_FOLDER)
