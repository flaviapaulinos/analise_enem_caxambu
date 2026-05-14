from evidently.report import Report
from evidently.presets import DataDriftPreset


def gerar_relatorio_drift(df_ref, df_atual):

    report = Report(metrics=[
        DataDriftPreset()
    ])

    report.run(
        reference_data=df_ref,
        current_data=df_atual
    )

    return report