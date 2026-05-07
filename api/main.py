from fastapi import FastAPI
import pandas as pd

from .schemas import InputENEM, OutputENEM
from .model_loader import get_model

app = FastAPI(
    title="API ENEM Caxambu",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "API ativa 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=OutputENEM)
def predict(data: InputENEM):

    model = get_model()

    # converter para DataFrame
    df = pd.DataFrame([data.dict()])

    # predição
    pred = model.predict(df)

    return {
        "nota_prevista": float(pred[0])
    }