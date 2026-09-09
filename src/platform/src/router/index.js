import { createRouter, createWebHashHistory } from 'vue-router'
import Courses from '../views/Courses.vue'
import Home from '../views/Home.vue'
import Module from '../views/Module.vue'
import Lesson from '../views/Lesson.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', name: 'courses', component: Courses },
    { path: '/:courseSlug', name: 'home', component: Home },
    { path: '/:courseSlug/:moduleDir', name: 'module', component: Module },
    { path: '/:courseSlug/:moduleDir/:lessonFile', name: 'lesson', component: Lesson },
  ],
})

export default router
