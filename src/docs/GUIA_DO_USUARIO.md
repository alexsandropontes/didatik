# 📖 Guia do Usuário — Didatik

Bem-vindo ao **Didatik**! Este manual foi criado para você que deseja planejar, escrever, organizar e disponibilizar cursos interativos e estruturados de alta qualidade pedagógica utilizando IA.

---

## 🎯 O que é o Didatik?

O Didatik é um framework educacional baseado na metodologia **Learn Run Fly (LRF)**:
* **🧠 Learn (Aprender):** O estudante compreende o conceito de forma clara, contextualizada e progressiva.
* **🏃 Run (Praticar):** Exercícios guiados passo a passo para colocar a mão na massa imediatamente.
* **🚀 Fly (Voar):** Desafios autônomos onde o estudante constrói soluções por conta própria.
* **📝 Quiz:** Fixação objetiva e interativa (4 a 6 perguntas por aula) que marca a aula como concluída após atingir $\ge 75\%$ de acerto.

O Didatik entrega:
1. **CLI no Terminal:** Gerencia templates, agentes de IA e a plataforma web de visualização.
2. **Squad de IA Especializado:** Agentes com funções pedagógicas estritas (`@teixeira`, `@cora`, `@andrade` e `@azevedo`).
3. **Plataforma Web Nativa (Vue 3):** Uma interface rápida e moderna para o aluno assistir às aulas, navegar entre módulos, responder quizzes interativos e acompanhar o progresso.

---

## 🚀 1. Instalação Rápida

O Didatik exige **Python 3.13+** e utiliza o gerenciador ultrarrápido [`uv`](https://docs.astral.sh/uv/).

### Instalando a ferramenta CLI:
```bash
uv tool install didatik
```
*(Ou tradicional via pip: `pip install didatik`)*

Verifique se a instalação funcionou:
```bash
didatik version
# 🎓 Didatik v1.0.0
```

---

## 🛠️ 2. Inicializando um Projeto de Cursos

Crie uma pasta para seus cursos e sincronize o runtime do Didatik:

```bash
mkdir meus-treinamentos
cd meus-treinamentos

# Sincroniza agentes, comandos, templates e a mini plataforma web:
didatik sync
```

O comando irá configurar a estrutura:
* `.agent/`: Prompts, agentes e comandos pedagógicos prontos para o seu assistente de IA.
* `cursos/`: Diretório onde todos os seus cursos serão criados.
* `platform/`: Aplicação web para exibir os cursos.
* `run.sh` / `run.ps1`: Scripts de execução com um clique.

---

## 🤖 3. Criando Cursos com os Agentes de IA

Abra o seu assistente de IA preferido no diretório do projeto (Claude Code, Cursor, Antigravity, OpenCode, etc.). 

O Didatik inclui comandos com o prefixo **`*dk`**:

### Criar um curso completo (de ponta a ponta)
```text
*dk course create "Curso completo de FastAPI para Iniciantes com foco em microsserviços"
```

O Didatik ativará o **Fluxo Canônico Automático**:
1. **`@azevedo`** inicia o projeto e chama o arquiteto pedagógico.
2. **`@teixeira` (Planejamento):** Analisa o público-alvo, define objetivos de aprendizagem com verbos observáveis, cria o syllabus e gera `cursos/<slug>/course.json` e os módulos `01/`, `02/`, etc.
3. **`@cora` (Escrita):** Escreve cada aula aplicando estritamente as seções **Learn**, **Run**, **Fly** e elabora o **Quiz** de fixação.
4. **`@andrade` (Quality Gate):** Revisa cada aula contra os **5 Pilares de Qualidade** (Coerência, Didática, Importância, Precisão e Engajamento). Se encontrar pendências, retorna a `@cora` para ajustes até atingir 100% de conformidade.

### Outros Comandos Úteis

| Comando | O que faz |
| :--- | :--- |
| `*dk course plan "<tema>"` | Apenas planeja o syllabus e estrutura as pastas, sem escrever as aulas ainda. |
| `*dk module create "<título>"` | Adiciona um novo módulo em um curso existente. |
| `*dk lesson create "<título>"` | Cria uma aula avulsa no formato LRF com quiz. |
| `*dk update course` | Ajusta ou enriquece um curso existente mantendo o isolamento dos demais. |
| `*dk help` | Lista os comandos disponíveis e orientações do squad. |

---

## 🌐 4. Visualizando o Curso na Plataforma Web

Para iniciar a plataforma e navegar pelas aulas como aluno:

### No Linux / macOS:
```bash
./run.sh
```

### No Windows (PowerShell):
```powershell
.\run.ps1
```

O script instala as dependências na primeira execução e abre automaticamente o navegador (geralmente em `http://localhost:5173`). 

---

## 📐 5. Entendendo a Estrutura de Arquivos (Contrato Multi-Curso)

Seus cursos residem organizados em pastas:

```text
cursos/
├── fastapi-iniciantes/              ← Slug do curso (máx. 50 caracteres)
│   ├── course.json                 ← Título, descrição, autor, duração e tags
│   ├── 01/                         ← Módulos são identificados por número de 2 dígitos
│   │   ├── module.json             ← Título e descrição do módulo
│   │   ├── assets/                 ← Imagens e diagramas daquele módulo
│   │   ├── 01-introducao.md        ← Aula com ciclo LRF + Quiz
│   │   └── 02-primeira-api.md
│   └── 02/
└── outro-curso/                    ← Outro treinamento isolado
```

### Validando a conformidade do curso
A qualquer momento você pode validar se suas aulas e módulos respeitam o contrato:
```bash
didatik validate
```
O validador checará se todos os schemas JSON são válidos, se as seções Learn, Run, Fly estão presentes e se os quizzes possuem as alternativas corretas configuradas.
