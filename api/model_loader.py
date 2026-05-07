import mlflow
from .config import MLFLOW_TRACKING_URI, MLFLOW_MODEL_URI

_model = None

def get_model():
    global _model

    if _model is None:
        print("🔄 Carregando modelo do MLflow...")

        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        _model = mlflow.pyfunc.load_model(MLFLOW_MODEL_URI)

        print("✅ Modelo carregado com sucesso!")

    return _model