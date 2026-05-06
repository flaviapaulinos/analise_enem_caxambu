from pydantic import BaseModel, Field

class InputENEM(BaseModel):
    renda: float = Field(..., ge=0, description="Renda familiar em salários mínimos")
    escola_publica: int = Field(..., ge=0, le=1)
    computador: int = Field(..., ge=0, le=1)
    internet: int = Field(..., ge=0, le=1)

class OutputENEM(BaseModel):
    nota_prevista: float