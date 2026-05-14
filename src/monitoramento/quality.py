from evidently.report import Report
from evidently.presets import DataQualityPreset


def gerar_relatorio_qualidade(df_ref, df_atual):

    report = Report(metrics=[
        DataQualityPreset()
    ])

    report.run(
        reference_data=df_ref,
        current_data=df_atual
    )

    return report