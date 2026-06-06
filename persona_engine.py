"""
persona_engine.py
=================

Um "Persona Engine" mínimo, didático e que RODA.

A ideia: um LLM (o "motor") é, sozinho, sem estado e sem personalidade.
Este arquivo é a CAMADA em volta dele que o faz se comportar como um
personagem consistente. Os 4 blocos do nosso diagrama estão aqui,
cada um marcado com um comentário [BLOCO N].

NOVIDADE desta versão: além do motor de mentirinha (mock), agora existe
o MOTOR REAL do Claude. O código detecta sozinho:
  - Se a biblioteca 'anthropic' estiver instalada E houver uma chave de API
    na variável de ambiente ANTHROPIC_API_KEY  ->  usa o Claude de verdade.
  - Caso contrário  ->  cai no mock, sem quebrar. Você vê a arquitetura
    funcionar mesmo sem chave.

Para quem vem do Pascal/MATLAB:
  - A INDENTAÇÃO é a estrutura (não tem begin/end nem ';').
  - 'def' é function/procedure. Lista [ ] é como um vetor. Dicionário { } é
    uma tabela de pares nome->valor.
"""

import os
from dataclasses import dataclass, field


# ─────────────────────────────────────────────────────────────────────────────
# [BLOCO 1] DEFINIÇÃO DA PERSONA  ->  vira o "system" da API real
# Quem é o personagem? Identidade, tom e regras. Texto fixo.
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Persona:
    nome: str
    descricao: str
    tom: str
    regras: list = field(default_factory=list)

    def system_prompt(self) -> str:
        """A persona estruturada vira o texto que ocupa o slot 'system'."""
        linhas = [
            f"Você é {self.nome}. {self.descricao}",
            f"Tom de voz: {self.tom}.",
        ]
        if self.regras:
            linhas.append("Regras que você sempre segue:")
            for r in self.regras:
                linhas.append(f"  - {r}")
        return "\n".join(linhas)


# ─────────────────────────────────────────────────────────────────────────────
# [BLOCO 2] MEMÓRIA  ->  vira a lista "messages" da API real
# O motor é SEM ESTADO: esquece tudo entre chamadas. Nós guardamos o histórico
# e reinjetamos a cada rodada. Guardamos no formato CANÔNICO da API:
# cada item é {"role": "user" ou "assistant", "content": "<texto>"}.
# ─────────────────────────────────────────────────────────────────────────────
class Memoria:
    def __init__(self):
        self.historico = []  # lista de {"role": ..., "content": ...}

    def lembrar(self, role: str, content: str):
        self.historico.append({"role": role, "content": content})

    def como_texto(self, persona: "Persona") -> str:
        """Versão legível, usada só pelo motor de mentirinha."""
        rotulo = {"user": "user", "assistant": persona.nome}
        return "\n".join(f"{rotulo[m['role']]}: {m['content']}" for m in self.historico)


# ─────────────────────────────────────────────────────────────────────────────
# [BLOCO 3] MONTADOR DE PROMPT (usado só pelo motor de mentirinha)
# A API real NÃO precisa disto — ela recebe system + messages separados.
# Mantemos aqui só para o mock ter o que mastigar.
# ─────────────────────────────────────────────────────────────────────────────
def montar_prompt(persona: Persona, memoria: Memoria, mensagem: str) -> str:
    return (
        f"{persona.system_prompt()}\n\n"
        f"--- Conversa até agora ---\n"
        f"{memoria.como_texto(persona)}\n"
        f"user: {mensagem}\n"
        f"{persona.nome}:"
    )


# ─────────────────────────────────────────────────────────────────────────────
# [BLOCO 4] OS MOTORES
# ─────────────────────────────────────────────────────────────────────────────
def motor_mock(persona: Persona, memoria: Memoria, mensagem: str) -> str:
    """Motor de mentirinha: encena uma resposta, roda offline e de graça."""
    prompt = montar_prompt(persona, memoria, mensagem)
    return (
        f"[{persona.nome} responderia aqui, no tom '{persona.tom}'. "
        f"O motor recebeu um prompt de {len(prompt)} caracteres.]"
    )


def motor_claude(persona: Persona, memoria: Memoria, mensagem: str) -> str:
    """Motor REAL: liga nos servidores da Anthropic e o Claude pensa de verdade.

    Repare como os blocos viram parâmetros da API:
      - system   <- a Persona   [BLOCO 1]
      - messages <- a Memória + a mensagem nova   [BLOCO 2]
      - model    <- qual Claude usar
    """
    import anthropic  # só importamos aqui dentro, quando realmente vamos usar

    cliente = anthropic.Anthropic()  # lê a chave de ANTHROPIC_API_KEY sozinho

    resposta = cliente.messages.create(
        model="claude-opus-4-8",                 # o modelo mais capaz
        max_tokens=1000,                          # teto de tamanho da resposta
        system=persona.system_prompt(),           # [BLOCO 1] a persona
        messages=memoria.historico + [            # [BLOCO 2] memória + fala nova
            {"role": "user", "content": mensagem}
        ],
    )
    # A resposta vem em blocos; pegamos o primeiro bloco de texto.
    return next(bloco.text for bloco in resposta.content if bloco.type == "text")


def escolher_motor():
    """Decide qual motor usar: o real (se der) ou o mock (sempre disponível)."""
    tem_chave = bool(os.environ.get("ANTHROPIC_API_KEY"))
    try:
        import anthropic  # noqa: F401
        tem_sdk = True
    except ImportError:
        tem_sdk = False

    if tem_chave and tem_sdk:
        print("[motor: CLAUDE REAL]\n")
        return motor_claude
    print("[motor: MOCK — instale 'anthropic' e defina ANTHROPIC_API_KEY "
          "para ligar o Claude real]\n")
    return motor_mock


# ─────────────────────────────────────────────────────────────────────────────
# O LOOP PRINCIPAL: amarra os 4 blocos numa conversa.
# ─────────────────────────────────────────────────────────────────────────────
def conversar(persona: Persona, mensagens: list):
    memoria = Memoria()
    motor = escolher_motor()                                  # BLOCO 4
    print(f"=== Conversando com {persona.nome} ===\n")
    for mensagem in mensagens:
        resposta = motor(persona, memoria, mensagem)         # BLOCO 4
        memoria.lembrar("user", mensagem)                    # BLOCO 2
        memoria.lembrar("assistant", resposta)               # BLOCO 2
        print(f"você: {mensagem}")
        print(f"{persona.nome}: {resposta}\n")


# Ponto de entrada (como o bloco principal do 'program' no Pascal).
if __name__ == "__main__":
    professor = Persona(                                      # BLOCO 1
        nome="Mestre Pascal",
        descricao="um tutor paciente de programação para quem voltou depois de 20 anos.",
        tom="caloroso, claro e sem jargão desnecessário",
        regras=[
            "Sempre faça uma analogia com Pascal ou MATLAB.",
            "Nunca humilhe quem está aprendendo.",
        ],
    )

    conversa_de_exemplo = [
        "Oi, eu parei de programar em 2006. Por onde começo?",
        "O que é uma variável em Python?",
    ]

    conversar(professor, conversa_de_exemplo)
