---

# ⚠️ CHECK: Quem executa este comando?

**Antes de prosseguir, responda:**
- Sou @azevedo agora?
- Identifiquei COM CERTEZA qual curso será alterado?

Curso não identificado → siga o Step 1 (disambiguação). NUNCA adivinhe.

---

name: dk-update-course
version: 1.0.0
author: "@azevedo"
---

# 🎯 *dk update course — Ajustes em Curso Existente

## Propósito

Aplica ajustes (conteúdo, estrutura, metadados) em um curso JÁ EXISTENTE, com garantia de **Isolamento de Curso** (Constituição, Seção II): nenhum outro curso é tocado.

## Pré-requisitos

- Pelo menos um curso em `cursos/` (com `course.json`)
- Descrição do ajuste desejado

## Processo

### Step 1: Identificar o Curso Alvo (OBRIGATÓRIO)

O usuário pode referenciar o curso por **slug** OU **título** (parcial conta).

1. Liste os cursos: leia `cursos/*/course.json` e monte `slug + título`.
2. Resolva a referência do usuário contra essa lista (slug exato > prefixo de slug > título contém).
3. **Se NENHUM ou VÁRIOS cursos matcharem** → apresente a tabela e PEÇA ao usuário para escolher:

   ```
   📚 Cursos encontrados — qual você quer ajustar?

   | # | Slug | Título |
   |---|------|--------|
   | 1 | python-basico | Python Básico |
   | 2 | python-dados | Python para Dados |

   Responda com o número, slug ou título.
   ```

4. **NUNCA prossiga sem o curso confirmado. NUNCA adivinhe.**

### Step 2: Roteamento do Ajuste

Com o curso alvo fixado (`cursos/<slug>/`), classifique o pedido:

| Tipo de ajuste | Agente | Processo |
|----------------|--------|----------|
| Novo módulo, reestruturação, mudança de objetivos/público | @teixeira | Skill `teixeira` (persistência DENTRO do curso alvo) |
| Ajuste de conteúdo de aula (texto, exemplos, quiz) | @cora | Skill `cora` (8 steps) + revisão @andrade |
| Avaliação de qualidade geral do curso | @andrade | Skill `andrade` (5 pilares, aula a aula) |

### Step 3: Executar com Isolamento

1. **Fixe o curso em contexto:** todo path de escrita DEVE começar com `cursos/<slug-alvo>/`.
2. Execute o processo da skill do agente escolhido.
3. **VETO:** nenhum arquivo fora de `cursos/<slug-alvo>/` pode ser criado, editado ou movido nesta operação.
4. Ajustes estruturais → @andrade revalida (syllabus ou aulas afetadas).

### Step 4: Consistência e Entrega

1. Revalide contagens do `course.json` e `module.json` do curso alvo.
2. Sugira `uv run scripts/validate_structure.py` (valida todos os cursos).
3. Relatório: o que mudou, em qual curso (slug + título), veredito de @andrade quando aplicável.

## Regras (NON-NEGOTIABLE)

1. **Isolamento absoluto:** escrever apenas dentro de `cursos/<slug-alvo>/`.
2. Ambiguidade = listar e perguntar. Nunca adivinhar.
3. Aula alterada passa por revisão @andrade de novo (mesmo veredito: 5 pilares 🟢).
4. Estrutura interna do curso segue a Constituição, Seção II.
