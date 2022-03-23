from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository
from mlflow.tracking import MlflowClient

client = MlflowClient()
my_model = client.download_artifacts("50616e30e0c74c4b95a5c6b2cb8c41b5", path="model")
print(f"Placed model in: {my_model}")