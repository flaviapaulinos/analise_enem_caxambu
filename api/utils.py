import pandas as pd

def to_dataframe(payload_dict: dict) -> pd.DataFrame:
    # alinhe nomes/ordem de colunas com o treino
    return pd.DataFrame([payload_dict])