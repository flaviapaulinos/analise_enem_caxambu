import os

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "https://dagshub.com/SEU_USUARIO/SEU_REPO.mlflow"
)

MLFLOW_MODEL_URI = os.getenv(
    "MLFLOW_MODEL_URI",
    "models:/enem_model/Production"  # ajuste para seu registry
)