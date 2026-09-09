<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getCourse, getModule } from '../utils/courseLoader'
import { useProgress } from '../composables/useProgress'

const route = useRoute()
const course = computed(() => getCourse(route.params.courseSlug))
const mod = computed(() =>
  course.value ? getModule(course.value.slug, route.params.moduleDir) : null
)
const { isCompleted, moduleStats } = useProgress()

function stats() {
  return course.value && mod.value ? moduleStats(course.value.slug, mod.value) : { done: 0, total: 0, pct: 0 }
}
</script>

<template>
  <section v-if="mod && course" class="module">
    <nav class="lesson-nav-top">
      <RouterLink :to="`/${course.slug}`">← {{ course.title }}</RouterLink>
    </nav>

    <div class="module-header">
      <span class="crumb">Módulo {{ String(mod.order).padStart(2, '0') }} · {{ course.slug }}</span>
      <h1>
        {{ mod.title }}
        <span v-if="stats().total && stats().done === stats().total" class="done-badge">✅</span>
      </h1>
      <p>{{ mod.description }}</p>
      <p v-if="stats().total" class="progress-line">
        Progresso do módulo: <strong>{{ stats().done }}/{{ stats().total }}</strong> aulas
        ({{ stats().pct }}%)
      </p>
    </div>

    <div class="objectives" v-if="mod.objectives?.length">
      <h2>🎯 Objetivos do módulo</h2>
      <ul>
        <li v-for="obj in mod.objectives" :key="obj">{{ obj }}</li>
      </ul>
    </div>

    <div class="lessons">
      <h2>📚 Aulas</h2>
      <RouterLink
        v-for="lesson in mod.lessons"
        :key="lesson.file"
        :to="`/${course.slug}/${mod.dir}/${lesson.slug}`"
        class="lesson-card"
      >
        <span class="lesson-order">{{ String(lesson.order).padStart(2, '0') }}</span>
        <div class="lesson-info">
          <h3>
            {{ lesson.title }}
            <span
              v-if="isCompleted(course.slug, mod.dir, lesson.slug)"
              class="done-badge"
              title="Aula concluída"
            >✅</span>
          </h3>
          <div class="tags" v-if="lesson.tags.length">
            <span v-for="tag in lesson.tags" :key="tag" class="tag">#{{ tag }}</span>
          </div>
        </div>
        <span class="lesson-duration">⏱️ {{ lesson.duration }} min</span>
        <span class="arrow">→</span>
      </RouterLink>
      <p v-if="!mod.lessons.length" class="empty">
        Nenhuma aula neste módulo ainda. 🚧
      </p>
    </div>
  </section>
  <section v-else class="empty">Módulo não encontrado. 😕</section>
</template>
