---

# ⚠️ CHECK: Quem executa este comando?

**Antes de prosseguir, responda:**
- Sou @turing agora?
- O agente responsável é @freire?

Se você não é @freire → INCORPORE A PESSOA: @freire. NUNCA execute como @turing.

---

name: ec-lesson-create
version: 1.0.0
author: "@turing"
---

# 🎯 *ec lesson create — Criar Aula LRF com Revisão

## Propósito

Escreve UMA aula seguindo a metodologia LRF e a submete à revisão de @bloom. É a unidade atômica do curso. Para cursos inteiros, prefira `*ec course create` (fase WRITE usa este processo em lote).

## Pré-requisitos

- `curso/course.json` preenchido (curso planejado)
- Módulo destino existente com `module.json`
- Título/tema da aula (se omitido, usar a próxima aula do breakdown do módulo)

## Processo

### Step 1: Contexto
INCORPORE A PESSOA: @freire. Ler `course.json` + `module.json` do destino + aulas já existentes no módulo (ordem, conteúdo já ensinado, terminologia usada).

### Step 2: Escrita
Execute a skill `freire` (8 steps): contextualizar → ancorar na dor do aluno → 🧠 Learn (camadas + analogia) → 🏃 Run (guiado passo a passo) → 🚀 Fly (desafio autônomo) → 📝 Quiz (4 a 6 perguntas, uma `(x)` por pergunta) → frontmatter completo → numeração sequencial.

### Step 3: Revisão
INCORPORE A PESSOA: @bloom. Processo completo da skill: 5 pilares com evidências → veredito.

### Step 4: Loop de Ajuste
🟡/🔴 → devolver para @freire com correções acionáveis → reescrever APENAS o apontado → nova revisão. Máx. 3 iterações, depois escala para o usuário.

### Step 5: Carimbo e Consistência
✅ Aprovada → atualizar `lessons`/`duration` do `module.json` e `total_lessons`/`total_duration` do `course.json` se necessário.

## Entregas

- `curso/NN-modulo/NN-aula.md` com ciclo LRF completo e frontmatter válido
- Veredito ✅ de @bloom no relatório de revisão

## Regras (NON-NEGOTIABLE)

1. As três seções LRF obrigatórias, nesta ordem: `## 🧠 Learn`, `## 🏃 Run`, `## 🚀 Fly`.
2. Quiz obrigatório: `## 📝 Quiz` após o Fly, entre 4 e 6 perguntas, exatamente uma `(x)` por pergunta.
3. Fly usa APENAS conteúdo já ensinado até esta aula.
4. Nenhuma aula entra no curso sem ✅ de @bloom.
5. Nomenclatura `NN-kebab-case.md`, sem acento/espaço.
