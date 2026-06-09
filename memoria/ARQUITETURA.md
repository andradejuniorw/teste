# 🏛️ Arquitetura da Memória

Documento que explica **o porquê** desta estrutura — a lógica de software por
trás da reorganização.

## Princípios

1. **Separação por responsabilidade (como módulos de código)**
   Perfil ≠ Projeto ≠ Conhecimento ≠ Decisão ≠ Rotina. Cada tipo de memória
   tem uma "responsabilidade única" e mora numa pasta só.

2. **Granularidade fina (arquivos pequenos e coesos)**
   Um arquivo gigante é como uma função de 2000 linhas: impossível de manter e
   de buscar. Arquivos pequenos = busca melhor pelos agentes e diffs limpos.

3. **Índice como fonte de navegação (como um roteador)**
   `00-indice/INDEX.md` é o ponto de entrada. Ninguém deveria precisar
   "adivinhar" onde está uma memória.

4. **Markdown sobre PDF (texto buscável sobre binário opaco)**
   Agentes leem Markdown com folga; PDF é binário e atrapalha a busca. Toda
   memória relevante vira `.md`.

5. **Versionado em Git (histórico = memória da memória)**
   Cada mudança fica registrada. Você consegue ver *quando* e *por que* uma
   memória mudou — algo que a memória global do app não te dá.

## Convenção de nomes

```
kebab-case-sem-acento.md
```

- Datas no formato ISO: `2026-06-09`.
- Decisões: `04-decisoes/0001-titulo-curto.md` (numeradas, estilo ADR).
- Projetos: `02-projetos/<nome-do-projeto>/README.md` + arquivos do tema.

## Ordem de migração (importante)

> ⚠️ **Refresh na memória global PRIMEIRO, limpeza de Drive DEPOIS.**
> Deletar pastas antigas **não** desfaz o que já foi consolidado na memória
> global. Inverter a ordem não funciona.

1. Exportar memória oficial (fonte da verdade).
2. Segmentar em `.md` aqui no repositório.
3. Revisar e validar contra o export.
4. Só então limpar/arquivar as pastas antigas no app/Drive.

## Fluxo de uma memória nova

```
ideia/fato novo
      │
      ▼
escolher template (_templates/)
      │
      ▼
criar arquivo na pasta certa (01..05)
      │
      ▼
registrar em 00-indice/INDEX.md
      │
      ▼
commit no Git
```
