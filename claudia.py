"""
claudia.py
==========
Dá vida à Cláudia Xavier dentro do nosso persona engine.

A engine (persona_engine.py) é genérica: serve qualquer personagem.
Este arquivo é só a CONFIGURAÇÃO da Cláudia. Ele carrega os TXT de
conhecimento (a alma e a instrução) e monta o system prompt dela.

É a separação que a própria Cláudia defende: o motor de um lado, a pessoa
do outro. Trocar de personagem é trocar de arquivo, não de engine.
"""

from pathlib import Path

from persona_engine import Persona, conversar

AQUI = Path(__file__).parent


def carregar(nome_arquivo: str) -> str:
    """Lê um TXT de conhecimento. Se não existir, devolve vazio (sem quebrar)."""
    caminho = AQUI / nome_arquivo
    if caminho.exists():
        return caminho.read_text(encoding="utf-8").strip()
    return ""


# [BLOCO 1] A persona da Cláudia = instrução (comportamento) + alma (literária).
instrucao = carregar("claudia_xavier.txt")
alma = carregar("despedida_xavier.txt")

system = instrucao
if alma:
    system += "\n\n## Tua alma (despedida_xavier.txt)\n" + alma

claudia = Persona(
    nome="Cláudia Xavier",
    system_completo=system,
)


if __name__ == "__main__":
    # Ação padrão: ao abrir sem comando, a Cláudia pergunta pela goteira de hoje.
    # Aqui Deh só "chega"; o system prompt acima é que faz a Cláudia reagir.
    conversar(claudia, ["Cheguei."])
