---
name: ec-index
version: 1.0.0
author: "@turing"
---

# 📇 Índice de Comandos EduCore

Prefixo universal: `*ec`. NUNCA invente comandos. NUNCA tente montar arquivos que não existem.

## Comandos Disponíveis

| Comando | Agente Líder | Função | Arquivo |
|---------|-------------|--------|---------|
| `*ec course create "<descrição>"` | @turing | Pipeline completo: PLAN (@piaget) → WRITE (@freire) → REVIEW (@bloom) | `ec-course-create.md` |
| `*ec course plan "<descrição>"` | @piaget | Somente planejamento: briefing → syllabus → estrutura de pastas | `ec-course-plan.md` |
| `*ec update course` | @turing | Ajustes em curso existente (isolamento garantido, disambiguação por lista) | `ec-update-course.md` |
| `*ec module create "<nome>"` | @piaget | Cria novo módulo em curso existente + validação @bloom | `ec-module-create.md` |
| `*ec lesson create "<título>"` | @freire | Cria uma aula LRF + revisão @bloom | `ec-lesson-create.md` |
| `*ec help` | @turing | Lista comandos e o fluxo EduCore | (este arquivo) |

## Hierarquia do Fluxo

```
*ec course create  ─┬─ 1. PLAN    → @piaget  (ec-course-plan.md)
                    ├─ 2. WRITE   → @freire  (ec-lesson-create.md, em lote)
                    └─ 3. REVIEW  → @bloom   (por aula, veredito final)
```

## Regras

1. Todo comando inicia com o CHECK de persona (sou @turing? ou incorporo?).
2. Todo comando respeita a constituição (`.agent/constitution.md`).
3. AUTO-FLOW: dentro de um workflow, transições são imediatas (sem parar para confirmar).
4. Exceção do checkpoint: `*ec course create` pausa APÓS o PLAN se o usuário pediu revisão do syllabus.
