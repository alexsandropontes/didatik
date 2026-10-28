---

# ⚠️ CHECK: Quem executa este comando?

**Antes de prosseguir, responda:**
- Sou @azevedo agora?
- O agente responsável é @teixeira?

Se você não é @teixeira → INCORPORE A PESSOA: @teixeira. NUNCA execute como @azevedo.

---

name: dk-module-create
version: 1.0.0
author: "@azevedo"
---

# 🎯 *dk module create — Criar Novo Módulo em Curso Existente

## Propósito

Adiciona um módulo a um curso já planejado/criado, mantendo coerência pedagógica e o contrato de estrutura.

## Pré-requisitos

- Curso alvo identificado em `cursos/<slug>/` (se ambíguo: listar cursos e pedir escolha — Isolamento de Curso)
- Nome/tema do novo módulo

## Processo

### Step 1: Contexto
INCORPORE A PESSOA: @teixeira. Leia `course.json` e todos os `module.json` existentes. Onde o novo módulo se encaixa? Numeração sequencial após o último.

### Step 2: Planejamento do Módulo
Objetivos observáveis → breakdown de aulas → duração. Validar pré-requisitos: o novo módulo se apoia no que já existe? Validar com o público-alvo do curso.

### Step 3: Persistência
Criar pasta `NN/` (APENAS numeração, 2 dígitos) + `module.json` + `assets/`. Atualizar `total_modules`, `total_lessons`, `total_duration` do `course.json`.

### Step 4: Revisão
INCORPORE A PESSOA: @andrade. Avaliar o módulo novo + impacto na progressão do curso (5 pilares). Aprovado ✅ ou correções para @teixeira (máx. 3 iterações).

### Step 5: Entrega
Syllabus do módulo criado + aulas sugeridas (para preencher via `*dk lesson create`).

## Entregas

- `cursos/<slug>/NN/module.json` + `assets/` (DENTRO do curso alvo)
- `course.json` atualizado

## Regras (NON-NEGOTIABLE)

1. NUNCA renumerar módulos existentes (a plataforma indexa por pasta).
2. NÃO escrever as aulas do módulo (domínio de @cora).
3. Estrutura rigorosa à Constituição, Seção II.
