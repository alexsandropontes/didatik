<script setup>
import { loadCourse } from '../utils/courseLoader'

const course = loadCourse()
</script>

<template>
  <section class="home">
    <div class="hero">
      <h1>{{ course.title }}</h1>
      <p class="subtitle">{{ course.subtitle }}</p>
      <p class="description">{{ course.description }}</p>
      <div class="meta">
        <span class="pill">👥 {{ course.audience }}</span>
        <span class="pill">📦 {{ course.modules.length }} módulos</span>
        <span class="pill">📚 {{ course.totalLessonsLoaded }} aulas</span>
        <span class="pill">⏱️ {{ course.total_duration }} min</span>
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
        :to="`/${mod.dir}`"
        class="module-card"
      >
        <span class="module-order">{{ String(mod.order).padStart(2, '0') }}</span>
        <div class="module-info">
          <h3>{{ mod.title }}</h3>
          <p>{{ mod.description }}</p>
          <span class="module-meta">
            📖 {{ mod.lessons.length }} aulas · ⏱️ {{ mod.duration }} min
          </span>
        </div>
        <span class="arrow">→</span>
      </RouterLink>
      <p v-if="!course.modules.length" class="empty">
        Nenhum módulo ainda. Use os agentes EduCore para criar o curso! 🎓
      </p>
    </div>
  </section>
</template>
