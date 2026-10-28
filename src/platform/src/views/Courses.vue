<script setup>
import { loadCourses } from '../utils/courseLoader'
import { useProgress } from '../composables/useProgress'

const courses = loadCourses()
const { courseStats } = useProgress()
</script>

<template>
  <section class="courses">
    <div class="hero">
      <h1>🎓 Meus Cursos</h1>
      <p class="description">
        {{ courses.length }} curso{{ courses.length === 1 ? '' : 's' }} — Learn Run Fly
      </p>
    </div>

    <RouterLink
      v-for="course in courses"
      :key="course.slug"
      :to="`/${course.slug}`"
      class="module-card course-card"
    >
      <div class="course-icon">📚</div>
      <div class="module-info">
        <h3>{{ course.title }}</h3>
        <p>{{ course.subtitle || course.description }}</p>
        <span class="module-meta">
          📦 {{ course.modules.length }} módulos · 📚 {{ course.totalLessonsLoaded }} aulas
          <template v-if="courseStats(course).total">
            · 🏆 {{ courseStats(course).done }}/{{ courseStats(course).total }}
            ({{ courseStats(course).pct }}%)
          </template>
        </span>
      </div>
      <span class="arrow">→</span>
    </RouterLink>

    <p v-if="!courses.length" class="empty">
      Nenhum curso ainda. Use os agentes Didatik para criar: *dk course create 🎓
    </p>
  </section>
</template>
