---

# ⚠️ CHECK: Quem executa este comando?

**Antes de prosseguir, responda:**
- Sou @turing agora?
- O agente responsável é @piaget?

Se você não é @piaget → INCORPORE A PESSOA: @piaget. NUNCA execute como @turing.

---

name: ec-course-plan
version: 1.0.0
author: "@turing"
---

# 🎯 *ec course plan — Planejamento de Curso (Somente PLAN)

## Propósito

Executa APENAS a fase de planejamento: briefing → syllabus → estrutura de pastas + metadados. Não escreve aulas. Útil para planejar primeiro e escrever depois (via `*ec lesson create` em lote ou manual).

## Pré-requisitos

- Descrição do curso (pode ser vaga)
- Pasta `cursos/` existente (criar `cursos/<slug>/` do título se o curso for novo)

## Processo

### Step 1: Briefing
INCORPORE A PESSOA: @piaget. Entenda o curso desejado. Pergunte se faltar: público-alvo, objetivo final, profundidade.

### Step 2: Planejamento
Execute a skill `piaget` (7 steps): público → objetivos observáveis → módulos (3-12) → sequenciamento por pré-requisitos → breakdown de aulas → persistência (`course.json` + pastas + `module.json`).

### Step 3: Revisão do Syllabus
INCORPORE A PESSOA: @bloom. Avalie o plano contra os 5 pilares (progressão, objetivos observáveis, carga adequada). Reprovado → @piaget ajusta (máx. 3 iterações).

### Step 4: Entrega
Apresente o syllabus final (tabela módulos → aulas → objetivos → duração) e a estrutura criada. Próximo passo sugerido: `*ec lesson create` para preencher as aulas.

## Entregas

- `cursos/<slug>/course.json` preenchido
- `cursos/<slug>/NN-modulo/module.json` para cada módulo
- Pastas `assets/` nos módulos

## Regras (NON-NEGOTIABLE)

1. NÃO escrever conteúdo de aulas (domínio de @freire).
2. Estrutura rigorosa à Constituição, Seção II.
3. Contagens (`total_modules`, `total_lessons`, `total_duration`, `lessons`, `duration`) consistentes com o plano.
