# 📐 STRUCTURE.md — O Contrato de Estrutura do Curso

Este documento é o **contrato** entre os agentes educacionais e a plataforma Vue. A plataforma lê a pasta `curso/` seguindo EXATAMENTE esta estrutura. Qualquer desvio quebra a renderização.

## Estrutura Canônica

```
curso/
├── course.json                    # OBRIGATÓRIO — metadados do curso
├── 01-nome-do-modulo/             # OBRIGATÓRIO — prefixo 2 dígitos + kebab-case
│   ├── module.json                # OBRIGATÓRIO — metadados do módulo
│   ├── assets/                    # OPCIONAL — imagens do módulo
│   │   └── exemplo.png
│   ├── 01-titulo-da-aula.md       # OBRIGATÓRIO — aula com ciclo LRF
│   └── 02-outra-aula.md
└── 02-proximo-modulo/
    ├── module.json
    ├── assets/
    └── 01-primeira-aula.md
```

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
```

**Obrigatório:** frontmatter completo (title, module, order, tags, duration) + as 3 seções LRF nesta ordem.

## Schemas

- `course-schema.json` — valida `curso/course.json`
- `module-schema.json` — valida `curso/NN-*/module.json`

## Validação

```bash
uv run scripts/validate_structure.py
```

Valida: schemas, nomenclatura, sequência numérica, seções LRF presentes, imagens referenciadas existem.
