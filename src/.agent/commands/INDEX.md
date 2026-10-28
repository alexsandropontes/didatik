---
name: dk-index
version: 1.0.0
author: "@azevedo"
---

# 📇 Índice de Comandos Didatik

Prefixo universal: `*dk`. NUNCA invente comandos. NUNCA tente montar arquivos que não existem.

## Comandos Disponíveis

| Comando | Agente Líder | Função | Arquivo |
|---------|-------------|--------|---------|
| `*dk course create "<descrição>"` | @azevedo | Pipeline completo: PLAN (@teixeira) → WRITE (@cora) → REVIEW (@andrade) | `dk-course-create.md` |
| `*dk course plan "<descrição>"` | @teixeira | Somente planejamento: briefing → syllabus → estrutura de pastas | `dk-course-plan.md` |
| `*dk update course` | @azevedo | Ajustes em curso existente (isolamento garantido, disambiguação por lista) | `dk-update-course.md` |
| `*dk module create "<nome>"` | @teixeira | Cria novo módulo em curso existente + validação @andrade | `dk-module-create.md` |
| `*dk lesson create "<título>"` | @cora | Cria uma aula LRF + revisão @andrade | `dk-lesson-create.md` |
| `*dk help` | @azevedo | Lista comandos e o fluxo Didatik | (este arquivo) |

## Hierarquia do Fluxo

```
*dk course create  ─┬─ 1. PLAN    → @teixeira  (dk-course-plan.md)
                    ├─ 2. WRITE   → @cora  (dk-lesson-create.md, em lote)
                    └─ 3. REVIEW  → @andrade   (por aula, veredito final)
```

## Regras

1. Todo comando inicia com o CHECK de persona (sou @azevedo? ou incorporo?).
2. Todo comando respeita a constituição (`.agent/constitution.md`).
3. AUTO-FLOW: dentro de um workflow, transições são imediatas (sem parar para confirmar).
4. Exceção do checkpoint: `*dk course create` pausa APÓS o PLAN se o usuário pediu revisão do syllabus.
