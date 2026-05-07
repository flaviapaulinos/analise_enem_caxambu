import os

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "https://dagshub.com/flaviapaulinos/analise_enem_caxambu.mlflow"
)

MLFLOW_MODEL_URI = os.getenv(
    "MLFLOW_MODEL_URI",
    "models:/enem_caxambu_produto/Production"
)