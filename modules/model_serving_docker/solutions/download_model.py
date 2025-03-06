import os
from pathlib import Path

import dotenv
import mlflow
from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository

project_root = Path(os.getenv("WORKSPACE_FOLDER", "/workspaces/llmops-course"))
dotenv.load_dotenv(project_root / ".env")

mlflow.set_tracking_uri(os.getenv("AZURE_MLFLOW_TRACKING_URI"))

# Get the latest production model
client = mlflow.tracking.MlflowClient()
model_versions = client.search_model_versions("name='article_summarizer'")
sorted_versions = sorted(model_versions, key=lambda x: int(x.version), reverse=True)

production_model = None
for version in sorted_versions:
    if "stage" in version.tags and version.tags["stage"] == "production":
        print(f"Production model found: {version.version}")
        print(
            f"Production Model URI:\n========\nmodels:/article_summarizer/{version.version}\n========"
        )
        break
else:
    raise Exception("No production model found")

model_uri = client.get_model_version_download_uri("article_summarizer", version.version)
print(f"Downloading model from {model_uri}")
# Download the model artifacts
ModelsArtifactRepository(
    f"models:/article_summarizer/{version.version}"
).download_artifacts(artifact_path="article_summarizer")
