<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getCourse } from '../utils/courseLoader'
import { useProgress } from '../composables/useProgress'

const route = useRoute()
const course = computed(() => getCourse(route.params.courseSlug))
const { moduleStats, courseStats } = useProgress()

function statsFor(mod) {
  return course.value ? moduleStats(course.value.slug, mod) : { done: 0, total: 0, pct: 0 }
}
</script>

<template>
  <section v-if="course" class="home">
    <nav class="lesson-nav-top">
      <RouterLink to="/">← Todos os cursos</RouterLink>
    </nav>

    <div class="hero">
      <h1>{{ course.title }}</h1>
      <p class="subtitle">{{ course.subtitle }}</p>
      <p class="description">{{ course.description }}</p>
      <div class="meta">
        <span class="pill">👥 {{ course.audience }}</span>
        <span class="pill">📦 {{ course.modules.length }} módulos</span>
        <span class="pill">📚 {{ course.totalLessonsLoaded }} aulas</span>
        <span class="pill">⏱️ {{ course.total_duration }} min</span>
        <span v-if="courseStats(course).total" class="pill">
          🏆 {{ courseStats(course).done }}/{{ courseStats(course).total }} concluídas
          ({{ courseStats(course).pct }}%)
        </span>
      </div>
      <div class="tags" v-if="course.tags?.length">
        <span v-for="tag in course.tags" :key="tag" class="tag">#{{ tag }}</span>
      </div>
    </div>

    <div class="objectives" v-if="course.objectives?.length">
      <h2>🎯 O que você vai aprender</h2>
      <ul>
        <li v-for="obj in course.objectives" :key="obj">{{ obj }}</li>
      </ul>
    </div>

    <div class="modules">
      <h2>🗺️ Módulos</h2>
      <RouterLink
        v-for="mod in course.modules"
        :key="mod.dir"
        :to="`/${course.slug}/${mod.dir}`"
        class="module-card"
      >
        <span class="module-order">{{ String(mod.order).padStart(2, '0') }}</span>
        <div class="module-info">
          <h3>
            {{ mod.title }}
            <span
              v-if="statsFor(mod).total && statsFor(mod).done === statsFor(mod).total"
              class="done-badge"
            >✅</span>
          </h3>
          <p>{{ mod.description }}</p>
          <span class="module-meta">
            📖 {{ mod.lessons.length }} aulas · ⏱️ {{ mod.duration }} min
            <template v-if="statsFor(mod).total">
              · ✅ {{ statsFor(mod).done }}/{{ statsFor(mod).total }} ({{ statsFor(mod).pct }}%)
            </template>
          </span>
        </div>
        <span class="arrow">→</span>
      </RouterLink>
      <p v-if="!course.modules.length" class="empty">
        Nenhum módulo ainda. Use os agentes EduCore para criar o curso! 🎓
      </p>
    </div>
  </section>
  <section v-else class="empty">Curso não encontrado. 😕</section>
</template>
