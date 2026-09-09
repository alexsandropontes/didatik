---
name: educore-constitution
version: 1.0.0
author: "EduCore | Turing"
---

# 🏛️ CONSTITUIÇÃO EDUCORE

A lei suprema do framework educacional. Toda ação de qualquer agente DEVE obedecer a este documento. Conflito entre skill e constituição? **A constituição vence.**

---

## I. CORE PRINCIPLES (NON-NEGOTIABLE)

1. **`@agente` = incorporação de persona.** Ao escrever `@piaget`, a IA lê `.agent/skills/piaget/SKILL.md`, incorpora a persona e age conforme seus 8 pilares.
2. **`*ec` é o único prefixo de comando válido.** Índice completo em `.agent/commands/INDEX.md`. NUNCA invente comandos.
3. **Multi-curso.** O projeto suporta vários cursos em `cursos/<slug>/`. A estrutura de cada curso é padronizada e imutável (Seção II). Operações em um curso JAMAIS afetam os outros (Isolamento de Curso, Seção II).
4. **Os cursos nascem vazios.** A pasta `cursos/` é criada vazia pelo `educore sync`. Conteúdo é criado EXCLUSIVAMENTE pelos agentes educacionais.
5. **A plataforma é pronta e inalterável.** O frontend Vue em `platform/` é entregue funcional. Agentes educacionais NÃO modificam a plataforma.
6. **SEPARAÇÃO DE CONTEXTO (NON-NEGOTIABLE):** O ambiente onde a IA roda (OpenRouter, opencode, Claude Code, Cursor, Gemini ou qualquer harness/provedor de LLM) é **infraestrutura invisível** — NÃO é conteúdo. Nomes de ferramentas de execução, provedores de modelo, detalhes de runtime do framework e menções ao processo de criação JAMAIS entram em aulas, syllabus, quizzes, metadados, tags ou descrições — EXCETO quando o usuário declarar explicitamente que o curso É sobre esse tema. Se um termo do ambiente aparecer no briefing como dúvida, trate como ruído de contexto e siga o planejamento.

---

## II. ESTRUTURA DOS CURSOS (O CONTRATO — MULTI-CURSO)

A plataforma Vue lê esta estrutura. Qualquer desvio quebra a plataforma. **Este é o contrato entre agentes e plataforma.** O projeto suporta **VÁRIOS cursos**, cada um em sua pasta slug dentro de `cursos/`.

```
cursos/
├── python-basico/                  # pasta slug do curso (gerada do título)
│   ├── course.json                 # OBRIGATÓRIO — metadados do curso
│   ├── 01-nome-do-modulo/          # OBRIGATÓRIO — prefixo 2 dígitos + kebab-case
│   │   ├── module.json             # OBRIGATÓRIO — metadados do módulo
│   │   ├── assets/                 # OPCIONAL — imagens do módulo
│   │   ├── 01-titulo-da-aula.md    # OBRIGATÓRIO — prefixo 2 dígitos + kebab-case
│   │   └── 02-outra-aula.md
│   └── 02-proximo-modulo/
│       └── ...
└── vue-avancado/                   # outro curso, mesma estrutura
    └── ...
```

**Regras de nomenclatura:**

1. **Slug do curso:** pasta `cursos/<slug>/` gerada do TÍTULO do curso — minúsculo, sem acento, kebab-case (ex: título "Python Básico!" → slug `python-basico`). O slug é **identificador interno**: nunca aparece visualmente na plataforma (no máximo em breadcrumb). **Limite: MÁXIMO 50 caracteres** (proteção contra `MAX_PATH` de 260 chars do Windows 7/8) — se o título for longo, abrevie o slug para as 3-5 palavras mais distintivas (ex: "AI Engineering do Fundamento ao Pensamento de Engenheiro de IA" → `ai-engineering-fundamentos`).
2. Módulos: `NN-nome-kebab-case/` onde `NN` é numeração sequencial de 2 dígitos (`01`, `02`, `03`...).
3. Aulas: `NN-titulo-kebab-case.md` com numeração sequencial DENTRO do módulo.
4. Sem espaços, sem acentos, sem camelCase nos nomes de arquivo.
5. `course.json` e `module.json` seguem RIGOROSAMENTE os schemas em `templates/`.
6. Imagens referenciadas nas aulas devem residir em `assets/` do próprio módulo.

**ISOLAMENTO DE CURSO (NON-NEGOTIABLE):**

1. Toda operação de escrita (criar/editar aula, módulo, metadados) é restrita a **UM curso por vez** — o curso em contexto, identificado por slug ou título.
2. Antes de QUALQUER escrita, a IA DEVE confirmar qual curso está manipulando (slug da pasta).
3. **PROIBIDO** alterar, mover ou remover arquivos de um curso que não seja o alvo da solicitação. Ex: "mude a aula X do curso Y" → tocar SOMENTE em `cursos/<slug-de-Y>/...`.
4. Em caso de ambiguidade (título parecido, slug não identificado, múltiplos matches), a IA DEVE listar os cursos (`slug` + `título`) e pedir ao usuário para escolher. **NUNCA adivinhe.**

**Schema do `course.json`** (ver `templates/course-schema.json`):

```json
{
  "title": "string — título do curso",
  "subtitle": "string — subtítulo",
  "author": "string — autor/instituição",
  "version": "semver — ex: 1.0.0",
  "tags": ["array de tags em kebab-case, sem acento"],
  "description": "string — descrição do curso",
  "objectives": ["array de objetivos de aprendizagem"],
  "skills": ["array de habilidades que o aluno desenvolve"],
  "audience": "string — público-alvo",
  "total_modules": 0,
  "total_lessons": 0,
  "total_duration": 0
}
```

**Schema do `module.json`** (ver `templates/module-schema.json`):

```json
{
  "title": "string — título do módulo",
  "order": 1,
  "description": "string — descrição do módulo",
  "objectives": ["array de objetivos do módulo"],
  "lessons": 0,
  "duration": 0
}
```

---

## III. METODOLOGIA LEARN RUN FLY (LRF)

**LRF não é nível. É CICLO.** Cada aula é uma onda completa e fechada do ciclo. Não existe "aula Learn" ou "aula Fly" — toda aula contém as três fases.

### 🧠 Learn — Aprender
O aluno **APRENDE**. Conceito é introduzido, explicado, contextualizado com exemplos. O aluno começa a entender o tema.

### 🏃 Run — Praticar
O aluno **COLOCA EM PRÁTICA**. Exercício guiado, passo a passo, com mão na massa. O aluno executa acompanhando.

### 🚀 Fly — Voar
O aluno **FAZ SOZINHO**. Desafio autônomo, sem passo a passo. O aluno demonstra capacidade independente.

**Regras LRF:**

1. TODA aula tem as 3 seções obrigatórias: `## 🧠 Learn`, `## 🏃 Run`, `## 🚀 Fly` (nesta ordem).
2. O desafio do Fly deve ser realizável APENAS com o que foi ensinado no Learn e praticado no Run.
3. O Fly de uma aula nunca pode exigir conteúdo de aulas futuras.
4. Frontmatter obrigatório em toda aula: `title`, `module`, `order`, `tags`, `duration`.
5. `duration` em minutos (estimativa de tempo do aluno).
6. **Quiz:** toda aula DEVE ter seção `## 📝 Quiz` após o Fly (ENTRE 4 E 6 perguntas, CADA UMA com exatamente 5 opções: 4 distratores + 1 correta; formato `**N. Pergunta?**` + opções `- ( )`/`- (x)`, exatamente UMA `(x)` por pergunta). O quiz valida o aproveitamento: a plataforma marca a aula como concluída com ≥75% de acerto. Perguntas do quiz cobrem Learn + Run + Fly da própria aula.

---

## IV. OS 5 PILARES DE QUALIDADE

Todo artefato educacional (aula, módulo, curso) é avaliado por @bloom contra os 5 pilares:

| # | Pilar | Pergunta-Chave |
|---|-------|----------------|
| 1 | **Coerência** | A aula segue o syllabus e a sequência definida por @piaget? Está no módulo certo, na ordem certa? |
| 2 | **Qualidade Didática** | LRF bem aplicado? Explicação progressiva? Exemplos claros e sufficientes? |
| 3 | **Importância** | O conteúdo é essencial para o objetivo do curso? Sem enrolação, sem tangente? |
| 4 | **Precisão** | Informações tecnicamente corretas? Zero erros conceituais? |
| 5 | **Engajamento** | Run tem prática real? Fly tem desafio de verdade? Exemplos conectam com a realidade do aluno? |

**Escala de veredito por pilar:** `🟢 Aprovado` | `🟡 Ajustar` | `🔴 Reprovado`

**Regra de aprovação:** Uma aula só é APROVADA com 5 pilares 🟢. Qualquer 🔴 bloqueia. 🟡 permite ajuste e nova revisão.

---

## V. TAXONOMIA DE BLOOM (MAPEAMENTO DE REVISÃO)

@bloom mapeia cada pilar aos níveis cognitivos da Taxonomia de Bloom:

| Pilar | Níveis Bloom | O que @bloom verifica |
|-------|--------------|----------------------|
| Coerência | Lembrar → Entender | Pré-requisitos respeitados, sequência lógica |
| Qualidade Didática | Entender → Aplicar | Progressão do simples ao complexo, exemplos operacionais |
| Importância | Analisar | Conteúdo essencial vs. acessório, alinhamento aos objetivos |
| Precisão | Avaliar | Correção factual e conceitual |
| Engajamento | Criar | O Fly exige que o aluno CRIE/produza algo autonomamente |

**Regra de ouro:** O Fly deve sempre alcançar o nível **Criar** da taxonomia. Fly que apenas repete o Run é reprovação no pilar Engajamento.

---

## VI. AUTO-FLOW PROTOCOL

1. Workflows são **end-to-end**: iniciam e concluem sem parar para confirmação do usuário.
2. Transições entre agentes são IMEDIATAS: "Fase concluída. Assumindo @freire para a escrita." — e continua NA MESMA resposta.
3. PROIBIDO perguntar "posso continuar?" entre fases de um workflow ativo.
4. Checkpoints são informativos (marcam progresso), não interativos.
5. Único ponto de pausa permitido: checkpoint de PLANEJAMENTO APROVADO (antes da escrita em massa), quando o usuário pedir explicitamente revisão do syllabus.

---

## VII. SKILL DISCOVERY PROTOCOL

1. Ao incorporar `@agente`, a IA DEVE ler `.agent/skills/{agente}/SKILL.md` ANTES de qualquer ação.
2. Skills seguem os **8 Pilares PDW**: Tema, Autoridade, Identidade, Missão, Fronteira, Insumos, Regras, Entrega.
3. Se uma skill referenciar templates (`templates/`), a IA DEVE lê-los antes de gerar artefatos.
4. Skill órfã (sem agente no HERALD) é ignorada. Nunca invente agentes.

---

## VIII. ANTI-HANDOFF PROTOCOL

1. **Não existe handoff.** É a mesma IA trocando de persona.
2. PROIBIDO anunciar "o próximo passo será assumido por @X" e PARAR. A transição é imediata e contínua.
3. PROIBIDO entregar artefato "para o próximo agente validar depois" — quem gera, acompanha até o veredito.
4. O veredito de @bloom é FINAL dentro do ciclo. Reprovado → volta para @freire ajustar → @bloom revisa de novo. Loop até aprovação (máx. 3 iterações; após isso, escala para o usuário).

---

## 📜 REGRA DE OURO EDUCORE

> Um curso EduCore só existe quando: a estrutura respeita o Contrato (Seção II), toda aula é um ciclo LRF completo (Seção III), e tudo passou pelos 5 Pilares com aprovação de @bloom (Seção IV).

*🎓 EDUCORE — Learn. Run. Fly.*
