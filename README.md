# 🎓 Didatik — Framework Educacional Learn Run Fly

Mini framework de governança para criação de **cursos interativos** com a metodologia **Learn Run Fly (LRF)**: cada aula é um ciclo fechado onde o aluno **APRENDE** (Learn), **PRATICA** (Run) e **VOA** (Fly).

Um squad de agentes de IA especializados planeja, escreve e revisa o curso; uma mini plataforma web (Vue 3) entrega o resultado pro aluno.

## 📦 Instalação

```bash
uv tool install didatik
```

*(ou via pip: `pip install didatik`)*

Requisito: **Python 3.13+**

## 🚀 Como usar

No diretório do seu curso:

```bash
didatik sync          # instala o runtime (.agent, CLAUDE.md, templates, scripts) + platform/
didatik sync --force  # atualiza o runtime existente (nunca toca em curso/)
didatik upgrade       # atualiza o motor global + re-sync do projeto
didatik validate      # valida o contrato de estrutura do curso
didatik version       # mostra a versão
```

Depois, com seu agente de IA (Claude Code, opencode, etc.) aberto no diretório do projeto:

```
*dk course create "curso de X"    # cria o curso completo, end-to-end
*dk course plan "curso de X"      # só planejamento (syllabus + estrutura)
*dk module create "nome"          # novo módulo em curso existente
*dk lesson create "título"        # cria uma aula LRF + revisão
*dk update course                 # ajustes em curso existente
```

### Plataforma web

```bash
cd platform && npm install && npm run dev
```

## 🤖 O Squad de Agentes

O Didatik funciona com um squad de 4 agentes de IA, cada um com autoridade estrita sobre seu domínio:

| Agente | Papel | Autoridade |
| :--- | :--- | :--- |
| **@azevedo** | Orchestrator Master | Orquestração geral e transições entre fases |
| **@teixeira** | Editor & Designer Instrucional | Syllabus, `course.json`, estrutura de módulos e objetivos |
| **@cora** | Writer & Roteirista Educacional | Conteúdo das aulas (`.md` com ciclo LRF) e quiz |
| **@andrade** | Revisor Pedagógico & Quality Gate | Veredito de qualidade pelos 5 Pilares (final) |

### Fluxo canônico

```
@azevedo → @teixeira (PLAN) → @cora (WRITE) → @andrade (REVIEW) → @azevedo (DONE)
```

### Os 5 Pilares de Qualidade (revisão do @andrade)

1. **Coerência** — segue o syllabus e a sequência do @teixeira
2. **Didática** — clareza, progressão e ciclo LRF completo
3. **Importância** — tudo no texto serve ao objetivo de aprendizagem
4. **Precisão** — exatidão técnica do conteúdo
5. **Engajamento** — analogias, contexto e prática significativa

## 🎓 Homenagem — quem são os nomes

Os agentes são uma homenagem a brasileiros cuja obra moldou a educação e a cultura do país:

- **Azevedo** — [Fernando de Azevedo](https://pt.wikipedia.org/wiki/Fernando_de_Azevedo) (1894–1974), educador paulista, líder do movimento escolanovista e reformador de sistemas de ensino. O grande articulador.
- **Teixeira** — [Anísio Teixeira](https://pt.wikipedia.org/wiki/An%C3%ADsio_Teixeira) (1900–1971), educador baiano, fundador do INEP e um dos construtores da escola pública brasileira. O arquiteto do planejamento.
- **Cora** — [Cora Coralina](https://pt.wikipedia.org/wiki/Cora_Coralina) (1889–1985), poetisa goiana, mestre da voz popular e acolhedora. A escritora das aulas.
- **Andrade** — [Mário de Andrade](https://pt.wikipedia.org/wiki/M%C3%A1rio_de_Andrade) (1893–1945), escritor, crítico e pesquisador paulista, figura central do Modernismo. O revisor rigoroso.

> **Aviso:** trata-se de **apenas uma homenagem**. Estas pessoas reais **não participaram do desenvolvimento do Didatik, não fazem parte do projeto e não endossam seu conteúdo**. Os handles usados no projeto (sobrenome para homens, primeiro nome para mulheres) existem apenas como apelidos de personas de software.

## 📁 Estrutura (Contrato — multi-curso)

```
projeto/
├── run.sh / run.ps1         # sobe a plataforma (zero fricção)
├── cursos/
│   └── <slug-do-curso>/     # ex.: python-basico/
│       ├── course.json      # metadados e syllabus
│       └── 01/              # módulo = apenas numeração
│           ├── module.json  # título e aulas do módulo
│           ├── assets/
│           └── 01-titulo-da-aula.md   # aula com ciclo LRF + quiz
├── platform/                # mini plataforma web (Vue 3)
├── .agent/                  # runtime do squad de agentes
└── templates/               # schemas do contrato
```

**Isolamento:** ajustes em um curso jamais tocam nos outros (`*dk update course` lista `slug + título` quando houver ambiguidade).

## 📚 Documentação completa

- [Manual do Usuário](src/docs/GUIA_DO_USUARIO.md) — instalação, comandos do squad e fluxo de criação de cursos
- [Manual do Desenvolvedor](src/docs/GUIA_DO_DESENVOLVEDOR.md) — arquitetura interna, plataforma Vue 3, empacotamento e padrões de contribuição

## 📄 Licença

MIT
