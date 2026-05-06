from fastapi import FastAPI
from .schemas import InputENEM, OutputENEM
from .model_loader import get_model
from .utils import to_dataframe

app = FastAPI(
    title="API ENEM Caxambu",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=OutputENEM)
def predict(data: InputENEM):
    model = get_model()
    df = to_dataframe(data.dict())
    pred = model.predict(df)
    return {"nota_prevista": float(pred[0])}