# 📐 STRUCTURE.md — O Contrato de Estrutura do Curso

Este documento é o **contrato** entre os agentes educacionais e a plataforma Vue. O projeto é **multi-curso**: a plataforma lê a pasta `cursos/`, onde cada subpasta slug é um curso. Qualquer desvio quebra a renderização.

## Estrutura Canônica (multi-curso)

```
cursos/
├── python-basico/                  ← slug do curso (gerado do título, sem acento)
│   ├── course.json                 # OBRIGATÓRIO — metadados do curso
│   ├── 01-nome-do-modulo/          # OBRIGATÓRIO — prefixo 2 dígitos + kebab-case
│   │   ├── module.json             # OBRIGATÓRIO — metadados do módulo
│   │   ├── assets/                 # OPCIONAL — imagens do módulo
│   │   │   └── exemplo.png
│   │   ├── 01-titulo-da-aula.md    # OBRIGATÓRIO — aula com ciclo LRF
│   │   └── 02-outra-aula.md
│   └── 02-proximo-modulo/
│       ├── module.json
│       ├── assets/
│       └── 01-primeira-aula.md
└── vue-avancado/                   ← outro curso, mesma estrutura
    └── ...
```

**Slug do curso:** gerado do título (minúsculo, sem acento, kebab-case), **máximo 50 caracteres** (títulos longos → abreviar para 3-5 palavras distintivas; proteção contra `MAX_PATH` de 260 chars no Windows 7/8). É identificador interno — nunca aparece visualmente na plataforma (no máximo em breadcrumb). Ex: "AI Engineering do Fundamento ao Pensamento de Engenheiro de IA" → `ai-engineering-fundamentos`.

**Isolamento:** operações em um curso jamais tocam nos outros. Ambiguidade → listar `slug + título` e pedir escolha (Constituição, Seção II).

## Regras de Nomenclatura

| Elemento | Regra | Exemplo |
|----------|-------|---------|
| Pasta de módulo | `NN-kebab-case` (2 dígitos, sem acento/espaço) | `03-trabalhando-com-listas` |
| Arquivo de aula | `NN-kebab-case.md` (2 dígitos, sequencial no módulo) | `05-metodos-de-lista.md` |
| Imagens | kebab-case dentro de `assets/` do módulo | `assets/diagrama-fluxo.png` |
| Tags | kebab-case, sem acento | `python`, `estruturas-de-dados` |

## Formato da Aula (`.md`)

```markdown
---
title: "Título da Aula"
module: 1
order: 2
tags: [tag1, tag2]
duration: 30
---

## 🧠 Learn

Conteúdo teórico em camadas, com analogias e exemplos progressivos.

## 🏃 Run

Exercício guiado, passo a passo, com resultado esperado em cada passo.

## 🚀 Fly

Desafio autônomo. Enunciado do que entregar, SEM passo a passo.

## 📝 Quiz

**1. Pergunta?**
- ( ) Opção errada
- (x) Opção correta — exatamente UMA marcada com (x)
```

**Obrigatório:** frontmatter completo (title, module, order, tags, duration) + as 3 seções LRF nesta ordem.

**Quiz (recomendado, vira componente interativo na plataforma):**

- Seção `## 📝 Quiz` APÓS o Fly, OPCIONAL (mas fortemente recomendada)
- ENTRE 4 E 6 perguntas, CADA UMA com exatamente 5 opções (4 distratores + 1 correta)
- Formato `**N. Pergunta?**` seguida de opções `- ( )` / `- (x)`
- Exatamente UMA opção `(x)` por pergunta (a correta)
- A aula é marcada como CONCLUÍDA quando o aluno atinge ≥75% no quiz
- Sem quiz, a aula não pode ser concluída na plataforma

## Schemas

- `course-schema.json` — valida `cursos/<slug>/course.json`
- `module-schema.json` — valida `cursos/<slug>/NN-*/module.json`

## Validação

```bash
uv run scripts/validate_structure.py
```

Valida: schemas, nomenclatura, sequência numérica, seções LRF presentes, imagens referenciadas existem.
