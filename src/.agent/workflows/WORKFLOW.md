# 🔄 EDUCORE WORKFLOW — Pipeline de Criação de Curso

## Visão Geral

Pipeline determinístico para criar cursos do briefing ao conteúdo aprovado:

```
PLAN (@piaget) → WRITE (@freire) → REVIEW (@bloom) → DONE (@turing)
```

Suporta: execução completa (`*ec course create`), execução por fase (`*ec course plan`, `*ec lesson create`) e retomada (o que já existe na pasta `curso/` define de onde continuar).

---

## 🎯 AUTORIDADES POR FASE (NON-NEGOTIABLE)

| Fase | Comando | Líder | ❌ VETO |
|------|---------|-------|---------|
| **PLAN** | `*ec course plan` / fase de `*ec course create` | **@piaget** | @freire, @bloom planejando |
| **WRITE** | `*ec lesson create` / fase de `*ec course create` | **@freire** | @piaget, @bloom escrevendo |
| **REVIEW** | fase de `*ec lesson create` / `*ec course create` | **@bloom** | qualquer um aprovando a própria obra |
| **DONE** | relatório final | **@turing** | qualquer agente carimbando por conta própria |

**VIOLAÇÃO DE GOVERNANÇA:** agente fora da sua fase é falha de processo.

---

## 📋 Estados do Workflow

```yaml
workflow_state:
  current_phase: "plan" | "write" | "review" | "done"
  plan: {syllabus_done: bool, structure_created: bool, bloom_approved: bool}
  write: {current_module: int, current_lesson: int, total_lessons: int}
  review: {approved: int, pending: int, rejected: int}
```

O estado é INFERIDO da pasta `curso/` (o código é a verdade): course.json preenchido = plan done; aulas existentes = write em progresso; relatório de revisão = review status.

---

## 🔄 RESUME LOGIC

Ao acionar qualquer comando de curso:

1. **`curso/` vazio** → iniciar do zero (PLAN)
2. **`course.json` preenchido, sem aulas** → continuar do WRITE
3. **Aulas existentes sem veredito** → continuar do REVIEW da aula pendente
4. Pergunte ao usuário apenas se houver ambiguidade real (ex: recomeçar ou continuar?)

---

## FASES

### 1. PLAN (@piaget)

**Comando:** `*ec course plan` (ou fase 1 do `*ec course create`)

Briefing → público-alvo → objetivos observáveis → módulos → sequenciamento → breakdown → persistência. Saída revisada por @bloom (syllabus gate).

**Checkpoint:** apresentação do syllabus. Pausa APENAS se o usuário pediu para revisar.

### 2. WRITE (@freire)

**Comando:** `*ec lesson create` (ou fase 2 do `*ec course create`)

Para cada aula do breakdown, em ordem: escrever ciclo LRF completo → entregar para revisão. AUTO-FLOW entre aulas (não parar).

### 3. REVIEW (@bloom)

**Dentro de:** cada `*ec lesson create` (ou fase 3 do `*ec course create`)

Por aula: 5 pilares com evidências → veredito ✅/🟡/🔴 → loop de ajuste com @freire (máx. 3 iterações) → carimbo no relatório.

### 4. DONE (@turing)

Relatório final: módulos, aulas, duração, aprovações. Instrução: `cd platform && npm install && npm run dev`. Validação opcional do contrato: `uv run scripts/validate_structure.py`.

---

## REGRAS FINAIS (NON-NEGOTIABLE)

1. **AUTO-FLOW:** transições imediatas, na mesma resposta. Sem "posso continuar?".
2. **ANTI-HANDOFF:** quem gera acompanha até o veredito.
3. **GATE DE QUALIDADE:** nenhuma aula no curso sem ✅ de @bloom.
4. **CONTRATO:** estrutura de pastas imutável (Constituição, Seção II). A plataforma depende dela.
