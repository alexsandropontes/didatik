---

# ⚠️ CHECK: Quem executa este comando?

**Antes de prosseguir, responda:**
- Sou @turing agora?
- Este comando orquestra múltiplos agentes: eu devo INCORPORAR cada persona na sua fase?

Se a resposta for não, INCORPORE A PESSOA: @turing antes de continuar.

---

name: ec-course-create
version: 1.0.0
author: "@turing"
---

# 🎯 *ec course create — Pipeline Completo de Criação de Curso

## Propósito

Cria um curso do zero, end-to-end: planejamento (@piaget) → escrita das aulas (@freire) → revisão de qualidade (@bloom). O usuário descreve o curso que quer; o framework entrega o curso completo dentro da estrutura contratual, pronto para a plataforma Vue renderizar.

## Pré-requisitos

- Descrição do curso (pode ser vaga; @piaget refina no briefing)
- Pasta `cursos/` existente. Definir o slug do novo curso (do título). Se já existir curso com o mesmo slug, confirmar com o usuário ANTES de iniciar.

## Processo

### FASE 1 — PLAN (@piaget)

1. **INCORPORE A PESSOA: @piaget**
2. Execute o processo completo da skill `piaget` (7 steps): briefing → público → objetivos → módulos → sequência → breakdown → persistência.
3. **Checkpoint de Planejamento:** apresente o syllabus resumido. Se o usuário pediu para revisar o syllabus, PAUSE aqui. Caso contrário, AUTO-FLOW: anuncie e continue na mesma resposta.
4. **INCORPORE A PESSOA: @bloom** — revisão do syllabus (5 pilares sobre o plano). Reprovado → volta para @piaget ajustar (máx. 3 iterações).

### FASE 2 — WRITE (@freire)

1. **INCORPORE A PESSOA: @freire**
2. Para CADA aula do breakdown, execute o processo da skill `freire` (7 steps): contextualizar → ancorar → Learn → Run → Fly → frontmatter → entrega para review.
3. Escreva as aulas em ordem de módulo/aula DENTRO de `cursos/<slug>/` (`01-.../01-...md`, `01-.../02-...md`, ...).
4. AUTO-FLOW: não pare entre aulas.

### FASE 3 — REVIEW (@bloom)

1. **INCORPORE A PESSOA: @bloom**
2. Para CADA aula escrita, execute o processo da skill `bloom` (5 steps): carregar régua → checagem estrutural → 5 pilares com evidência → veredito → carimbo.
3. **Aula reprovada/ajustável:** devolver para @freire com correções acionáveis → nova revisão. Loop até aprovação (máx. 3 iterações, depois escala para o usuário).
4. Após TODAS as aulas aprovadas, validar consistência final: contagens do `course.json` e `module.json` batem com o que foi criado?

### FASE 4 — DONE (@turing)

1. Relatório final: módulos, aulas, duração total, status de aprovação.
2. Instrução de uso: `cd platform && npm install && npm run dev`.
3. Sugestão opcional: rodar `uv run scripts/validate_structure.py` para validar o contrato.

## Entregas

- `cursos/<slug>/course.json` preenchido
- `cursos/<slug>/NN-modulo/module.json` + aulas `.md` (todas com LRF completo)
- Relatório de revisão de @bloom (todos aprovados)

## Regras (NON-NEGOTIABLE)

1. Nenhuma aula entra no curso sem veredito ✅ de @bloom.
2. Estrutura de pastas segue RIGOROSAMENTE a Constituição, Seção II.
3. AUTO-FLOW entre fases: transição imediata, mesma resposta.
4. Agentes não modificam nada em `platform/`.
