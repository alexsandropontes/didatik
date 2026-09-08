<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { loadCourse } from './utils/courseLoader'

const route = useRoute()
const course = loadCourse()

const isHome = computed(() => route.name === 'home')
</script>

<template>
  <div class="app">
    <header class="header" v-if="!isHome">
      <RouterLink to="/" class="back">← {{ course.title }}</RouterLink>
    </header>
    <main class="main">
      <RouterView />
    </main>
    <footer class="footer">
      <span>🎓 {{ course.title }} · Learn Run Fly</span>
    </footer>
  </div>
</template>
