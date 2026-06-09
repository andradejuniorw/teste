# 🧠 Memória — Ecossistema Claude

Repositório-modelo para **exportar, segmentar e reorganizar** a memória do seu
ecossistema Claude com lógica de software (versionável em Git).

> Substitui a bagunça das 50+ pastas que cresceram organicamente por uma
> arquitetura limpa, onde **cada memória tem um lugar previsível**.

## Como usar (fluxo)

1. **Exporte a fonte da verdade:** no app Claude → *Configurações → Privacy →
   Export data*. Esse arquivo é o espelho **fiel e completo** da sua memória.
   (O "dump" gerado por uma conversa é só rascunho — não é completo.)
2. **Segmente:** quebre o conteúdo em arquivos `.md` finos — **um tema por
   arquivo** — usando os modelos em [`_templates/`](_templates/).
3. **Realoque:** distribua cada arquivo na pasta certa (veja abaixo).
4. **Converta PDFs:** transforme os PDFs de memória em Markdown e guarde em
   [`03-conhecimento/`](03-conhecimento/) — Markdown é muito mais buscável pelos
   agentes de pasta do que PDF.
5. **Indexe:** registre cada arquivo novo em
   [`00-indice/INDEX.md`](00-indice/INDEX.md).

## Estrutura

| Pasta | O que guarda |
|---|---|
| [`00-indice/`](00-indice/) | Índice mestre de tudo. O ponto de entrada. |
| [`01-perfil/`](01-perfil/) | Quem você é, preferências, jeito de trabalhar, identidade. |
| [`02-projetos/`](02-projetos/) | Uma subpasta por projeto. Migre aqui as 50+ pastas. |
| [`03-conhecimento/`](03-conhecimento/) | Base de referência. PDFs convertidos em Markdown. |
| [`04-decisoes/`](04-decisoes/) | Log de decisões (o "porquê" das escolhas). Estilo ADR. |
| [`05-rotinas/`](05-rotinas/) | Fluxos recorrentes, processos, SOPs. |
| [`_templates/`](_templates/) | Modelos para criar arquivos novos com padrão. |

## Regras de ouro

- **Um tema por arquivo.** Se um tema crescer, divida em dois — não force.
- **Nome do arquivo = o tema.** `kebab-case`, sem acento: `preferencias-de-escrita.md`.
- **Todo arquivo começa com front-matter** (veja os templates).
- **Atualizou algo? Atualize o INDEX.** O índice é a única fonte de navegação.
