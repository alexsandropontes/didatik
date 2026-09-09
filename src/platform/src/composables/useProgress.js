import { reactive, watch } from 'vue'

const STORAGE_KEY = 'educore:progress:v2'

function load() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}
  } catch {
    return {}
  }
}

// Estrutura: { "<courseSlug>/<moduleDir>/<lessonSlug>": { completed, score } }
const progress = reactive(load())

watch(
  progress,
  (val) => localStorage.setItem(STORAGE_KEY, JSON.stringify(val)),
  { deep: true }
)

export function useProgress() {
  function keyFor(courseSlug, moduleDir, lessonSlug) {
    return `${courseSlug}/${moduleDir}/${lessonSlug}`
  }

  function isCompleted(courseSlug, moduleDir, lessonSlug) {
    return Boolean(progress[keyFor(courseSlug, moduleDir, lessonSlug)]?.completed)
  }

  function getScore(courseSlug, moduleDir, lessonSlug) {
    return progress[keyFor(courseSlug, moduleDir, lessonSlug)]?.score ?? null
  }

  function markCompleted(courseSlug, moduleDir, lessonSlug, score) {
    progress[keyFor(courseSlug, moduleDir, lessonSlug)] = { completed: true, score }
  }

  function resetLesson(courseSlug, moduleDir, lessonSlug) {
    delete progress[keyFor(courseSlug, moduleDir, lessonSlug)]
  }

  function moduleStats(courseSlug, mod) {
    const total = mod.lessons?.length || 0
    const done =
      mod.lessons?.filter((l) => isCompleted(courseSlug, mod.dir, l.slug)).length || 0
    return { done, total, pct: total ? Math.round((done / total) * 100) : 0 }
  }

  function courseStats(course) {
    const total = course.modules?.reduce((acc, m) => acc + (m.lessons?.length || 0), 0) || 0
    const done =
      course.modules?.reduce((acc, m) => acc + moduleStats(course.slug, m).done, 0) || 0
    return { done, total, pct: total ? Math.round((done / total) * 100) : 0 }
  }

  return { isCompleted, getScore, markCompleted, resetLesson, moduleStats, courseStats }
}
