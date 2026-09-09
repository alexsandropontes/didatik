<script setup>
import { loadCourses } from './utils/courseLoader'

const courses = loadCourses()
const brand = courses.length ? 'EduCore' : 'EduCore — Learn Run Fly'
</script>

<template>
  <div class="app">
    <header class="header">
      <RouterLink to="/" class="brand">🎓 {{ brand }}</RouterLink>
    </header>
    <main class="main">
      <RouterView />
    </main>
    <footer class="footer">
      <span>🎓 EduCore · Learn Run Fly</span>
    </footer>
  </div>
</template>
