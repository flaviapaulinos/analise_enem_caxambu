from pydantic import BaseModel, Field
from typing import Literal

class InputENEM(BaseModel):

    SalMin: Literal[
        'até 1', '1 a 3', '3 a 5',
        '5 a 10', '10 a 15', '15 a 20', 'acima de 20'
    ]

    Escola: Literal[
        'pública', 'não informada', 'privada'
    ]

    OcupPaisMedia: float
    EscolaridadePaisMedia: float
    Cel: float
    Comptdr: float
    PessoasResd: float


class OutputENEM(BaseModel):
    nota_prevista: float