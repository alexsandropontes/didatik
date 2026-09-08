---

# ⚠️ CHECK: Quem executa este comando?

**Antes de prosseguir, responda:**
- Sou @turing agora?
- O agente responsável é @piaget?

Se você não é @piaget → INCORPORE A PESSOA: @piaget. NUNCA execute como @turing.

---

name: ec-module-create
version: 1.0.0
author: "@turing"
---

# 🎯 *ec module create — Criar Novo Módulo em Curso Existente

## Propósito

Adiciona um módulo a um curso já planejado/criado, mantendo coerência pedagógica e o contrato de estrutura.

## Pré-requisitos

- `curso/course.json` existente e preenchido
- Nome/tema do novo módulo

## Processo

### Step 1: Contexto
INCORPORE A PESSOA: @piaget. Leia `course.json` e todos os `module.json` existentes. Onde o novo módulo se encaixa? Numeração sequencial após o último.

### Step 2: Planejamento do Módulo
Objetivos observáveis → breakdown de aulas → duração. Validar pré-requisitos: o novo módulo se apoia no que já existe? Validar com o público-alvo do curso.

### Step 3: Persistência
Criar pasta `NN-nome-kebab-case/` + `module.json` + `assets/`. Atualizar `total_modules`, `total_lessons`, `total_duration` do `course.json`.

### Step 4: Revisão
INCORPORE A PESSOA: @bloom. Avaliar o módulo novo + impacto na progressão do curso (5 pilares). Aprovado ✅ ou correções para @piaget (máx. 3 iterações).

### Step 5: Entrega
Syllabus do módulo criado + aulas sugeridas (para preencher via `*ec lesson create`).

## Entregas

- `curso/NN-novo-modulo/module.json` + `assets/`
- `course.json` atualizado

## Regras (NON-NEGOTIABLE)

1. NUNCA renumerar módulos existentes (a plataforma indexa por pasta).
2. NÃO escrever as aulas do módulo (domínio de @freire).
3. Estrutura rigorosa à Constituição, Seção II.
