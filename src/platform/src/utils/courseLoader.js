// Importa estaticamente TODOS os cursos (Contrato Didatik multi-curso).
// Estrutura: cursos/<slug>/{course.json, NN-modulo/{module.json, aulas.md}}
// Funciona em dev e em build sem backend: os cursos são embutidos no bundle.
const courseFiles = import.meta.glob('../../../cursos/*/course.json', { eager: true })
const moduleFiles = import.meta.glob('../../../cursos/*/*/module.json', { eager: true })
const lessonFiles = import.meta.glob('../../../cursos/*/*/*.md', {
  eager: true,
  query: '?raw',
  import: 'default',
})

function parseFrontmatter(raw) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/)
  if (!match) return { data: {}, body: raw }
  const data = {}
  for (const line of match[1].split(/\r?\n/)) {
    const idx = line.indexOf(':')
    if (idx === -1) continue
    const key = line.slice(0, idx).trim()
    let value = line.slice(idx + 1).trim()
    if (value.startsWith('[')) {
      value = value
        .replace(/[[\]]/g, '')
        .split(',')
        .map((t) => t.trim().replace(/^["']|["']$/g, ''))
        .filter(Boolean)
    } else {
      value = value.replace(/^["']|["']$/g, '')
    }
    data[key] = value
  }
  const body = raw.slice(match[0].length).trim()
  return { data, body }
}

function slugify(name) {
  return name.replace(/^\d+-/, '')
}

function buildCourse(slug, courseJson) {
  const course = { slug, ...courseJson, modules: [], totalLessonsLoaded: 0 }

  const mods = Object.entries(moduleFiles)
    .filter(([path]) => path.split('/').at(-3) === slug)
    .map(([path, mod]) => {
      const dir = path.split('/').at(-2)
      return { dir, slug: slugify(dir), order: Number(dir.slice(0, 2)), ...mod.default }
    })
    .sort((a, b) => a.order - b.order)

  const lessons = Object.entries(lessonFiles)
    .filter(([path]) => path.split('/').at(-3) === slug)
    .map(([path, raw]) => {
      const parts = path.split('/')
      const moduleDir = parts.at(-3) === slug ? parts.at(-2) : null
      const file = parts.at(-1)
      const { data, body } = parseFrontmatter(raw)
      return {
        moduleDir,
        file,
        slug: file.replace(/\.md$/, ''),
        body,
        title: data.title || slugify(file.replace(/\.md$/, '')),
        order: Number(data.order ?? Number(file.slice(0, 2))),
        tags: Array.isArray(data.tags) ? data.tags : [],
        duration: Number(data.duration || 0),
      }
    })

  for (const m of mods) {
    m.lessons = lessons
      .filter((l) => l.moduleDir === m.dir)
      .sort((a, b) => a.order - b.order)
  }
  course.modules = mods
  course.totalLessonsLoaded = lessons.length
  return course
}

let cache = null

export function loadCourses() {
  if (cache) return cache
  cache = Object.entries(courseFiles)
    .map(([path, mod]) => {
      const slug = path.split('/').at(-2)
      return buildCourse(slug, mod.default)
    })
    .sort((a, b) => String(a.title).localeCompare(String(b.title), 'pt-BR'))
  return cache
}

export function getCourse(courseSlug) {
  return (
    loadCourses().find((c) => c.slug === courseSlug) ||
    loadCourses().find((c) => c.slug.startsWith(courseSlug)) ||
    null
  )
}

export function getModule(courseSlug, moduleSlug) {
  const course = getCourse(courseSlug)
  if (!course) return null
  return (
    course.modules.find((m) => m.dir === moduleSlug || m.slug === moduleSlug) ||
    course.modules.find((m) => m.slug.startsWith(moduleSlug)) ||
    null
  )
}

export function getLesson(courseSlug, moduleSlug, lessonSlug) {
  const mod = getModule(courseSlug, moduleSlug)
  if (!mod) return null
  const lesson =
    mod.lessons.find((l) => l.slug === lessonSlug) ||
    mod.lessons.find((l) => l.slug.startsWith(lessonSlug)) ||
    null
  if (!lesson) return null
  const idx = mod.lessons.indexOf(lesson)
  return {
    ...lesson,
    courseSlug,
    module: mod,
    prev: mod.lessons[idx - 1] || null,
    next: mod.lessons[idx + 1] || null,
  }
}

// Divide o corpo da aula nas 3 seções LRF + quiz (opcional)
export function splitLrf(body) {
  const sections = { learn: '', run: '', fly: '', quiz: '' }
  const learnMatch = body.match(/##\s*🧠\s*Learn([\s\S]*?)(?=##\s*🏃|$)/)
  const runMatch = body.match(/##\s*🏃\s*Run([\s\S]*?)(?=##\s*🚀|$)/)
  const flyMatch = body.match(/##\s*🚀\s*Fly([\s\S]*?)(?=##\s*📝|$)/)
  const quizMatch = body.match(/##\s*📝\s*Quiz([\s\S]*)$/)
  if (learnMatch) sections.learn = learnMatch[1].trim()
  if (runMatch) sections.run = runMatch[1].trim()
  if (flyMatch) sections.fly = flyMatch[1].trim()
  if (quizMatch) sections.quiz = quizMatch[1].trim()
  return sections
}

// Parseia a seção Quiz em estrutura de dados:
// **1. Pergunta?** seguida de "- (x)" (correta) e "- ( )" (erradas)
export function parseQuiz(quizBlock) {
  if (!quizBlock) return null
  const questions = []
  const qRe = /\*\*\d+\.\s*(.+?)\*\*\r?\n([\s\S]*?)(?=\*\*\d+\.|\s*$)/g
  let qMatch
  while ((qMatch = qRe.exec(quizBlock)) !== null) {
    const prompt = qMatch[1].trim()
    const options = []
    let answer = -1
    const optRe = /^-\s*\(([ xX])\)\s*(.+)$/gm
    let oMatch
    while ((oMatch = optRe.exec(qMatch[2])) !== null) {
      if (oMatch[1].toLowerCase() === 'x') answer = options.length
      options.push(oMatch[2].trim())
    }
    if (prompt && options.length >= 2 && answer >= 0) {
      questions.push({ prompt, options, answer })
    }
  }
  return questions.length ? questions : null
}
