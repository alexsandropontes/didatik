# 🎓 EduCore — Framework Educacional Learn Run Fly

Mini framework de governança para criação de cursos interativos com a metodologia **Learn Run Fly (LRF)**: cada aula é um ciclo fechado onde o aluno **APRENDE** (Learn), **PRATICA** (Run) e **VOA** (Fly).

## Instalação

```bash
uv tool install --python 3.13 git+ssh://git@github.com/lxptech/educore.git
```

## Uso

No diretório do seu curso:

```bash
educore sync          # instala runtime (.agent, CLAUDE.md, templates, scripts) + platform/
educore sync --force  # atualiza runtime existente (nunca toca curso/)
educore upgrade       # atualiza o motor global + re-sync
educore validate      # valida o contrato de estrutura do curso
```

Depois, com seu agente de IA (Claude Code, opencode, etc.) no diretório:

```
*ec course create "curso de X"   # pipeline: @piaget → @freire → @bloom
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

**Isolamento:** ajustes em um curso jamais tocam nos outros (`*ec update course` lista `slug + título` quando ambíguo).

## Agentes

| Agente | Papel |
|--------|-------|
| `@piaget` | Editor & Designer Instrucional (syllabus) |
| `@freire` | Writer & Roteirista (aulas LRF) |
| `@bloom` | Revisor Pedagógico (5 Pilares de Qualidade) |
