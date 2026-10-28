# 💻 Guia do Desenvolvedor — Didatik

Este manual é destinado a desenvolvedores, mantenedores e colaboradores que desejam entender a arquitetura do **Didatik**, customizar suas funcionalidades, contribuir com melhorias ou evoluir a mini plataforma web e os agentes de IA.

---

## 🏛️ 1. Arquitetura do Repositório

O Didatik é organizado em módulos desacoplados no diretório `src/`:

```text
src/
├── didatik/                ← Pacote Python principal (CLI, sync, upgrade)
│   ├── cli.py             ← Comandos Typer (sync, upgrade, validate, version)
│   ├── entrypoint.py      ← Entry point com checagem de runtime Python 3.13+
│   └── sync.py            ← Engine de empacotamento e sincronização de templates
├── platform/              ← Single Page Application em Vue 3 + Vite
│   ├── src/
│   │   ├── components/    ← QuizSection.vue e componentes reativos
│   │   ├── composables/   ← useProgress.js (estado e localStorage)
│   │   ├── utils/         ← courseLoader.js (import.meta.glob de cursos e markdown)
│   │   └── views/         ← Home.vue, Courses.vue, Module.vue, Lesson.vue
│   └── vite.config.js     ← Configuração do bundler
├── .agent/                ← Runtime dos agentes educacionais (prompts e comandos)
│   ├── constitution.md    ← Regras de conformidade e contrato do framework
│   ├── HERALD.md          ← Roster de agentes (@azevedo, @teixeira, @cora, @andrade)
│   ├── commands/          ← Comandos *dk (dk-course-create.md, etc.)
│   └── skills/            ← Definição das competências instrucionais de cada persona
├── templates/             ← Schemas JSON e templates padrão de cursos e aulas
│   ├── course-schema.json
│   ├── module-schema.json
│   └── lesson-template.md
├── scripts/               ← Utilitários de validação (validate_structure.py)
├── hatch_build.py         ← Hook de build personalizado para empacotar o registry
└── pyproject.toml         ← Metadados do pacote Python e dependências
```

---

## ⚙️ 2. Ambiente de Desenvolvimento Local

### Pré-requisitos
* **Python 3.13+** (recomendado usar [`uv`](https://docs.astral.sh/uv/))
* **Node.js 18+** e **npm**

### Configurando o ambiente Python
Clone o repositório e crie um ambiente virtual na raiz de `src/`:
```bash
cd src
uv venv --python 3.13
source .venv/bin/activate

# Instala as dependências de desenvolvimento e o pacote em modo editável:
uv pip install -e .
```

Teste o comando CLI localmente:
```bash
didatik --help
```

### Configurando a Plataforma Vue
```bash
cd src/platform
npm install
npm run dev
```
A plataforma rodará localmente com Hot Module Replacement (HMR).

---

## 📦 3. Como Funciona o Build e Distribuição

O Didatik utiliza o **Hatchling** com um hook customizado em [`hatch_build.py`](file:///home/lexpontes/projetos/_treinamentos/prepara-treinamento/src/hatch_build.py).

### O Registry Embutido
Quando o pacote `didatik` é empacotado em wheel (`.whl`), os seguintes artefatos são copiados para dentro de `didatik/registry/`:
* `.agent/`
* `CLAUDE.md`
* `templates/`
* `scripts/`
* `platform/` (excluindo `node_modules` e `dist`)
* `run.sh` e `run.ps1`

Quando o usuário roda `didatik sync`, a função `sync_runtime` em [`didatik/sync.py`](file:///home/lexpontes/projetos/_treinamentos/prepara-treinamento/src/didatik/sync.py) extrai esses recursos via `importlib.resources` para o diretório local do usuário, preservando pastas protegidas como `cursos/`.

Para gerar a build de distribuição:
```bash
cd src
uv run python -m build
```

---

## 🎨 4. Plataforma Web (Vue 3)

### `courseLoader.js` (Carregador Dinâmico e Estático)
* A plataforma lê os arquivos Markdown e JSON usando Vite `import.meta.glob`:
  ```javascript
  const courseFiles = import.meta.glob('../../../cursos/*/course.json', { eager: true })
  const moduleFiles = import.meta.glob('../../../cursos/*/*/module.json', { eager: true })
  const lessonFiles = import.meta.glob('../../../cursos/*/*/*.md', { eager: true, query: '?raw', import: 'default' })
  ```
* Isso permite que a plataforma rode tanto em desenvolvimento quanto compilada como SPA estática (`npm run build`), embutindo os cursos diretamente no bundle sem necessitar de uma API backend.

### Parser LRF e Quizzes
* A função `splitLrf(body)` divide a aula nas seções canônicas: `learn`, `run`, `fly` e `quiz`.
* A função `parseQuiz(quizBlock)` interpreta a sintaxe Markdown de perguntas com opções `- ( )` e `- (x)`.

---

## 🧪 5. Validação e Qualidade de Código

### Validador Estrutural
O validador [`scripts/validate_structure.py`](file:///home/lexpontes/projetos/_treinamentos/prepara-treinamento/src/scripts/validate_structure.py) checa:
1. Conformidade de `course.json` e `module.json` contra schemas JSON.
2. Nomenclatura das pastas (módulos como `01`, `02` com máx. 30 chars; aulas com máx. 40 chars; slugs com máx. 50 chars).
3. Presença das seções `## 🧠 Learn`, `## 🏃 Run` e `## 🚀 Fly`.
4. Regras do Quiz (entre 4 e 6 perguntas, 5 alternativas cada, exatamente 1 correta).

Para rodar a validação:
```bash
python scripts/validate_structure.py [caminho-para-cursos]
```

---

## 🤝 6. Padrões de Contribuição e Git

* **Commits Atômicos:** Descreva o que foi alterado e o porquê (ex: `feat(cli): adiciona flag --quiet`, `fix(platform): ajusta layout em telas móveis`).
* **Branching Model:**
  * `dev-working-ia`: Branch local para experimentos e desenvolvimento assistido por IA (**nunca sobe para o GitHub**).
  * `dev`: Branch de integração e testes aprovados.
  * `main`: Branch oficial de lançamento estável.
* **Dados Pessoais & Segredos:** Nunca comite arquivos `.env`, chaves de API, credenciais ou diretórios de harnesses locais.
