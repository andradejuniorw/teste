"""
persona_engine.py
=================

Um "Persona Engine" mínimo, didático e que RODA.

A ideia: um LLM (o "motor") é, sozinho, sem estado e sem personalidade.
Este arquivo é a CAMADA em volta dele que o faz se comportar como um
personagem consistente. Os 4 blocos do nosso diagrama estão aqui,
cada um marcado com um comentário [BLOCO N].

Para quem vem do Pascal/MATLAB:
  - Não tem 'begin/end' nem ';' no fim da linha. A INDENTAÇÃO é a estrutura.
  - 'def' é o que você chamava de 'function'/'procedure'.
  - Uma lista [ ... ] é como um vetor do MATLAB, mas pode guardar qualquer coisa.
  - Um dicionário { "chave": valor } é uma tabela de pares nome->valor.
"""

from dataclasses import dataclass, field


# ─────────────────────────────────────────────────────────────────────────────
# [BLOCO 1] DEFINIÇÃO DA PERSONA
# Quem é o personagem? Isto é o "system prompt": um texto fixo que descreve
# identidade, tom e regras. É o equivalente a inicializar as variáveis globais
# do programa antes de tudo começar.
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Persona:
    nome: str
    descricao: str          # quem ele é, em uma frase
    tom: str                # como ele fala
    regras: list = field(default_factory=list)  # o que ele sempre/nunca faz

    def system_prompt(self) -> str:
        """Transforma a persona estruturada em um texto que o motor entende."""
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
# [BLOCO 2] MEMÓRIA
# O motor é SEM ESTADO (stateless): esquece tudo entre uma chamada e outra,
# igual a uma função pura. Então NÓS guardamos o histórico aqui e reinjetamos
# a cada rodada. Esta lista é a "RAM" do personagem.
# ─────────────────────────────────────────────────────────────────────────────
class Memoria:
    def __init__(self):
        self.historico = []  # cada item: {"papel": "user"/"assistant", "texto": "..."}

    def lembrar(self, papel: str, texto: str):
        self.historico.append({"papel": papel, "texto": texto})

    def como_texto(self) -> str:
        return "\n".join(f"{m['papel']}: {m['texto']}" for m in self.historico)


# ─────────────────────────────────────────────────────────────────────────────
# [BLOCO 3] MONTADOR DE PROMPT (o orquestrador)
# Junta  Persona + Memória + mensagem nova  em UMA entrada para o motor.
# ─────────────────────────────────────────────────────────────────────────────
def montar_prompt(persona: Persona, memoria: Memoria, mensagem: str) -> str:
    return (
        f"{persona.system_prompt()}\n\n"
        f"--- Conversa até agora ---\n"
        f"{memoria.como_texto()}\n"
        f"user: {mensagem}\n"
        f"{persona.nome}:"
    )


# ─────────────────────────────────────────────────────────────────────────────
# [BLOCO 4] O MOTOR (LLM)
# Esta é a única peça que você NÃO escreve de verdade — na vida real é a API
# do Claude. Aqui usamos um "motor de mentirinha" (mock) para você ver a
# arquitetura funcionando offline, sem precisar de chave de API ainda.
# Mais pra frente trocamos só esta função pela chamada real ao Claude.
# ─────────────────────────────────────────────────────────────────────────────
def motor_mock(prompt: str, persona: Persona) -> str:
    """Devolve uma resposta encenada, só para provar que os blocos se conectam."""
    return (
        f"[{persona.nome} responderia aqui, no tom '{persona.tom}'. "
        f"O motor recebeu um prompt de {len(prompt)} caracteres com toda a "
        f"persona e a memória embutidas.]"
    )


# ─────────────────────────────────────────────────────────────────────────────
# O LOOP PRINCIPAL: amarra os 4 blocos numa conversa.
# ─────────────────────────────────────────────────────────────────────────────
def conversar(persona: Persona, mensagens: list):
    memoria = Memoria()
    print(f"=== Conversando com {persona.nome} ===\n")
    for mensagem in mensagens:
        prompt = montar_prompt(persona, memoria, mensagem)   # BLOCO 3
        resposta = motor_mock(prompt, persona)               # BLOCO 4
        memoria.lembrar("user", mensagem)                    # BLOCO 2
        memoria.lembrar(persona.nome, resposta)              # BLOCO 2
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
