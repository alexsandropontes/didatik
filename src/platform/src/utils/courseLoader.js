import courseJson from '../../../curso/course.json'

// Importa estaticamente a estrutura do curso (Contrato EduCore).
// Funciona em dev e em build sem backend: o curso é embutido no bundle.
const moduleFiles = import.meta.glob('../../../curso/*/module.json', { eager: true })
const lessonFiles = import.meta.glob('../../../curso/*/*.md', {
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

function loadModules() {
  const modules = Object.entries(moduleFiles).map(([path, mod]) => {
    const dir = path.split('/').at(-2)
    return {
      dir,
      slug: slugify(dir),
      order: Number(dir.slice(0, 2)),
      ...mod.default,
    }
  })
  return modules.sort((a, b) => a.order - b.order)
}

function loadLessons(modules) {
  const lessons = Object.entries(lessonFiles).map(([path, raw]) => {
    const parts = path.split('/')
    const moduleDir = parts.at(-2)
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
  for (const m of modules) {
    m.lessons = lessons
      .filter((l) => l.moduleDir === m.dir)
      .sort((a, b) => a.order - b.order)
  }
  return lessons
}

let cache = null

export function loadCourse() {
  if (cache) return cache
  const modules = loadModules()
  const lessons = loadLessons(modules)
  cache = {
    ...courseJson,
    modules,
    totalLessonsLoaded: lessons.length,
  }
  return cache
}

export function getModule(moduleSlug) {
  const course = loadCourse()
  return (
    course.modules.find((m) => m.dir === moduleSlug || m.slug === moduleSlug) ||
    course.modules.find((m) => m.slug.startsWith(moduleSlug)) ||
    null
  )
}

export function getLesson(moduleSlug, lessonSlug) {
  const mod = getModule(moduleSlug)
  if (!mod) return null
  const lesson =
    mod.lessons.find((l) => l.slug === lessonSlug) ||
    mod.lessons.find((l) => l.slug.startsWith(lessonSlug)) ||
    null
  if (!lesson) return null
  const idx = mod.lessons.indexOf(lesson)
  return {
    ...lesson,
    module: mod,
    prev: mod.lessons[idx - 1] || null,
    next: mod.lessons[idx + 1] || null,
  }
}

// Divide o corpo da aula nas 3 seções LRF
export function splitLrf(body) {
  const sections = { learn: '', run: '', fly: '' }
  const learnMatch = body.match(/##\s*🧠\s*Learn([\s\S]*?)(?=##\s*🏃|$)/)
  const runMatch = body.match(/##\s*🏃\s*Run([\s\S]*?)(?=##\s*🚀|$)/)
  const flyMatch = body.match(/##\s*🚀\s*Fly([\s\S]*)$/)
  if (learnMatch) sections.learn = learnMatch[1].trim()
  if (runMatch) sections.run = runMatch[1].trim()
  if (flyMatch) sections.fly = flyMatch[1].trim()
  return sections
}
