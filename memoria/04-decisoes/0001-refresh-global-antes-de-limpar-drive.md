---
numero: 0001
titulo: "Refresh na memória global antes de limpar o Drive"
status: "aceita"
data: "2026-06-09"
---

# 0001 — Refresh na memória global antes de limpar o Drive

## Contexto
Ao reorganizar as 50+ pastas de projeto, surgiu a dúvida sobre a ordem das
operações: limpar primeiro as pastas/Drive ou atualizar a memória global.

## Decisão
**Atualizar (refresh) a memória global PRIMEIRO. Limpar o Drive/pastas DEPOIS.**

## Consequências
- ✅ Evita perda de contexto: deletar pastas antigas **não** desfaz o que já
  foi consolidado na memória global, então limpar antes não "resolve" nada e
  ainda pode confundir.
- ✅ A fonte da verdade (export oficial da memória) é capturada antes de
  qualquer remoção.
- ⚠️ Inverter a ordem não funciona — é a armadilha a evitar.
