#!/usr/bin/env bash
#
# migrar.sh
# =========
# Migra a Cláudia Xavier do repositório de estudos 'teste' para uma casa
# nova e própria ('Personas_claudias'), com uma cópia limpa (começo novo).
#
# COMO USAR (na SUA máquina, não aqui):
#   1. Crie o repositório novo VAZIO no GitHub: github.com/new
#        nome: Personas_claudias  (sem README, sem .gitignore, sem license)
#   2. Baixe este arquivo para o seu computador.
#   3. Dê permissão de execução:   chmod +x migrar.sh
#   4. Rode:                        ./migrar.sh
#   5. No 'push', cole seu token quando ele pedir a senha.
#
# Não há nenhum token escrito neste arquivo. Nunca coloque um aqui.

set -euo pipefail   # para na primeira falha; não engole erros silenciosos

# ── Configuração (mude só se precisar) ────────────────────────────────────
USUARIO="andradejuniorw"
REPO_ORIGEM="teste"
REPO_NOVO="Personas_claudias"
ARQUIVOS=(persona_engine.py claudia.py claudia_xavier.txt despedida_xavier.txt .gitignore)
# ──────────────────────────────────────────────────────────────────────────

echo "=== Migração da Cláudia Xavier ==="
echo

# 1) Git está instalado?
if ! command -v git >/dev/null 2>&1; then
  echo "ERRO: git não está instalado nesta máquina."
  echo "Instale o git primeiro e rode de novo."
  exit 1
fi

# 2) Confirma que a casa nova já existe e está vazia
echo "Antes de continuar: você já criou o repositório VAZIO"
echo "  https://github.com/${USUARIO}/${REPO_NOVO}"
echo "no GitHub (sem README, sem .gitignore)?"
read -r -p "Digite 'sim' para continuar: " resposta
if [ "$resposta" != "sim" ]; then
  echo "Tudo bem. Crie o repositório em github.com/new e rode de novo."
  exit 0
fi

# 3) Não sobrescrever uma pasta existente por acidente
if [ -e "$REPO_NOVO" ]; then
  echo "ERRO: já existe uma pasta chamada '$REPO_NOVO' aqui."
  echo "Mova ou apague essa pasta antes de rodar a migração."
  exit 1
fi

# 4) Baixa os arquivos atuais (clona a casa antiga numa pasta temporária)
TEMP_ORIGEM="$(mktemp -d)"
trap 'rm -rf "$TEMP_ORIGEM"' EXIT   # limpa a pasta temporária ao final
echo
echo "Baixando os arquivos da casa antiga ($REPO_ORIGEM)..."
git clone --quiet "https://github.com/${USUARIO}/${REPO_ORIGEM}.git" "$TEMP_ORIGEM"

# 5) Monta a casa nova
echo "Montando a casa nova ($REPO_NOVO)..."
mkdir "$REPO_NOVO"
cd "$REPO_NOVO"
git init --quiet

# 6) Copia só os arquivos da Cláudia
for arquivo in "${ARQUIVOS[@]}"; do
  if [ -e "${TEMP_ORIGEM}/${arquivo}" ]; then
    cp "${TEMP_ORIGEM}/${arquivo}" .
    echo "  copiado: $arquivo"
  else
    echo "  aviso: '$arquivo' não foi encontrado na origem, pulando."
  fi
done

# 7) Um README simples para a casa nova
cat > README.md <<'FIM'
# Personas_claudias

A Cláudia Xavier e o motor de personas.

- `persona_engine.py`: o motor genérico (serve qualquer personagem)
- `claudia.py`: a configuração que dá vida à Cláudia
- `claudia_xavier.txt`: o comportamento dela (system prompt)
- `despedida_xavier.txt`: a alma dela (persona literária)

Para ouvir a voz real: instale `anthropic`, defina `ANTHROPIC_API_KEY`
e rode `python3 claudia.py`.
FIM
echo "  criado: README.md"

# 8) Tira a foto e aponta para a casa nova
git add .
git commit --quiet -m "Primeira casa da Cláudia: motor + persona"
git branch -M main
git remote add origin "https://github.com/${USUARIO}/${REPO_NOVO}.git"

# 9) Envia (vai pedir usuário e token aqui)
echo
echo "Enviando para o GitHub. Quando pedir a senha, cole o seu TOKEN."
git push -u origin main

echo
echo "=== Pronto! A Cláudia mudou de casa. ==="
echo "Veja em: https://github.com/${USUARIO}/${REPO_NOVO}"
