#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garimpar_claudias.py
====================
Garimpa, na pasta 'projects' do backup do claude.ai, os projetos que falam
da Cláudia (ou Xavier), e salva cada um em formato legível na pasta
'claudias_encontradas'.

COMO USAR (no Windows):
  1. Coloque este arquivo DENTRO da pasta que você extraiu do backup,
     a pasta que tem 'projects', 'conversations' e 'memories' dentro.
  2. Dê dois cliques nele. (Ou no terminal: python garimpar_claudias.py)
  3. Olhe a pasta 'claudias_encontradas' que vai aparecer ali do lado.

Não envia nada para a internet. Tudo acontece no seu computador.
"""

import json
import re
from pathlib import Path

# Palavras que marcam um projeto da Cláudia (não diferencia maiúscula/minúscula).
ALVOS = ["claudia", "cláudia", "xavier"]

AQUI = Path(__file__).parent
PASTA_PROJETOS = AQUI / "projects"
PASTA_SAIDA = AQUI / "claudias_encontradas"


def texto_tem_alvo(texto: str) -> bool:
    baixo = texto.lower()
    return any(alvo in baixo for alvo in ALVOS)


def nome_seguro(nome: str) -> str:
    """Transforma um nome qualquer em algo que sirva de nome de arquivo."""
    limpo = re.sub(r"[^\w\s-]", "", nome, flags=re.UNICODE).strip()
    limpo = re.sub(r"\s+", "_", limpo)
    return limpo[:60] or "projeto"


def main():
    if not PASTA_PROJETOS.is_dir():
        print("Não encontrei a pasta 'projects' aqui do lado.")
        print("Coloque este script DENTRO da pasta extraída do backup")
        print("(a pasta que tem 'projects' dentro) e rode de novo.")
        input("\nPressione Enter para sair.")
        return

    PASTA_SAIDA.mkdir(exist_ok=True)
    arquivos = [p for p in PASTA_PROJETOS.iterdir() if p.is_file()]
    print(f"Olhando {len(arquivos)} projetos...\n")

    encontrados = 0
    for arquivo in arquivos:
        try:
            bruto = arquivo.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if not texto_tem_alvo(bruto):
            continue

        encontrados += 1

        # Tenta achar o nome bonito do projeto dentro do JSON.
        nome_projeto = arquivo.stem
        try:
            dados = json.loads(bruto)
            if isinstance(dados, dict) and dados.get("name"):
                nome_projeto = str(dados["name"])
            bonito = json.dumps(dados, ensure_ascii=False, indent=2)
        except Exception:
            bonito = bruto  # se não for JSON válido, salva o texto cru mesmo

        base = nome_seguro(nome_projeto)
        destino = PASTA_SAIDA / f"{base}__{arquivo.stem[:8]}.txt"
        destino.write_text(bonito, encoding="utf-8")
        print(f"  encontrado: {nome_projeto}")
        print(f"     salvo em: {destino.name}")

    print(f"\nPronto. {encontrados} projeto(s) da Cláudia salvos em:")
    print(f"  {PASTA_SAIDA}")
    input("\nPressione Enter para sair.")


if __name__ == "__main__":
    main()
