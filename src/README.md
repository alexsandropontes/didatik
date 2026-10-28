# 🎓 Didatik — Framework Educacional Learn Run Fly

Mini framework de governança para criação de cursos interativos com a metodologia **Learn Run Fly (LRF)**: cada aula é um ciclo fechado onde o aluno **APRENDE** (Learn), **PRATICA** (Run) e **VOA** (Fly).

## Instalação

```bash
uv tool install didatik
```

*(Ou via pip: `pip install didatik`)*

## Uso

No diretório do seu curso:

```bash
didatik sync          # instala runtime (.agent, CLAUDE.md, templates, scripts) + platform/
didatik sync --force  # atualiza runtime existente (nunca toca curso/)
didatik upgrade       # atualiza o motor global + re-sync
didatik validate      # valida o contrato de estrutura do curso
```

Depois, com seu agente de IA (Claude Code, opencode, etc.) no diretório:

```
*dk course create "curso de X"   # pipeline: @teixeira → @cora → @andrade
```

## Plataforma

```bash
cd platform && npm install && npm run dev
```

## Estrutura (Contrato — multi-curso)

```
cursos/
├── python-basico/          ← slug do curso (gerado do título)
│   ├── course.json
│   └── 01/                 ← módulo = APENAS numeração
│       ├── module.json     ← título do módulo aqui
│       ├── assets/
│       └── 01-titulo-da-aula.md   # aula com ciclo LRF + quiz
└── vue-avancado/           ← outro curso
```

**Isolamento:** ajustes em um curso jamais tocam nos outros (`*dk update course` lista `slug + título` quando ambíguo).

## Agentes

| Agente | Papel |
|--------|-------|
| `@teixeira` | Editor & Designer Instrucional (syllabus) |
| `@cora` | Writer & Roteirista (aulas LRF) |
| `@andrade` | Revisor Pedagógico (5 Pilares de Qualidade) |

## 📚 Documentação Completa

* **[Manual do Usuário](file:///home/lexpontes/projetos/_treinamentos/prepara-treinamento/src/docs/GUIA_DO_USUARIO.md):** Guia passo a passo de instalação, comandos do squad e fluxo de criação de cursos.
* **[Manual do Desenvolvedor](file:///home/lexpontes/projetos/_treinamentos/prepara-treinamento/src/docs/GUIA_DO_DESENVOLVEDOR.md):** Arquitetura interna, desenvolvimento da plataforma Vue 3, empacotamento Hatchling e padrões de contribuição.

