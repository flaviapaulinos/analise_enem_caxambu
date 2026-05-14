from pathlib import Path


def salvar_html(report, nome_arquivo):

    pasta = Path("relatorios/evidently")
    pasta.mkdir(parents=True, exist_ok=True)

    caminho = pasta / nome_arquivo

    report.save_html(str(caminho))

    print(f"Relatório salvo em: {caminho}")