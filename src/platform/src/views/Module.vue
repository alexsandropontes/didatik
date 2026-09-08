<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getModule } from '../utils/courseLoader'

const route = useRoute()
const mod = computed(() => getModule(route.params.moduleDir))
</script>

<template>
  <section v-if="mod" class="module">
    <div class="module-header">
      <span class="crumb">Módulo {{ String(mod.order).padStart(2, '0') }}</span>
      <h1>{{ mod.title }}</h1>
      <p>{{ mod.description }}</p>
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
        :to="`/${mod.dir}/${lesson.slug}`"
        class="lesson-card"
      >
        <span class="lesson-order">{{ String(lesson.order).padStart(2, '0') }}</span>
        <div class="lesson-info">
          <h3>{{ lesson.title }}</h3>
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
