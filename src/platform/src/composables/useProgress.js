import { reactive, watch } from 'vue'

const STORAGE_KEY = 'educore:progress:v1'

function load() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}
  } catch {
    return {}
  }
}

// Estrutura: { "01-modulo/01-aula": { completed: bool, score: number } }
const progress = reactive(load())

watch(
  progress,
  (val) => localStorage.setItem(STORAGE_KEY, JSON.stringify(val)),
  { deep: true }
)

export function useProgress() {
  function keyFor(moduleDir, lessonSlug) {
    return `${moduleDir}/${lessonSlug}`
  }

  function isCompleted(moduleDir, lessonSlug) {
    return Boolean(progress[keyFor(moduleDir, lessonSlug)]?.completed)
  }

  function getScore(moduleDir, lessonSlug) {
    return progress[keyFor(moduleDir, lessonSlug)]?.score ?? null
  }

  function markCompleted(moduleDir, lessonSlug, score) {
    progress[keyFor(moduleDir, lessonSlug)] = { completed: true, score }
  }

  function resetLesson(moduleDir, lessonSlug) {
    delete progress[keyFor(moduleDir, lessonSlug)]
  }

  function moduleStats(mod) {
    const total = mod.lessons?.length || 0
    const done = mod.lessons?.filter((l) => isCompleted(mod.dir, l.slug)).length || 0
    return { done, total, pct: total ? Math.round((done / total) * 100) : 0 }
  }

  function courseStats(course) {
    const total = course.modules?.reduce((acc, m) => acc + (m.lessons?.length || 0), 0) || 0
    const done = course.modules?.reduce(
      (acc, m) => acc + moduleStats(m).done,
      0
    ) || 0
    return { done, total, pct: total ? Math.round((done / total) * 100) : 0 }
  }

  return { isCompleted, getScore, markCompleted, resetLesson, moduleStats, courseStats }
}
