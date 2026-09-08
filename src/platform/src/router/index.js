import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Module from '../views/Module.vue'
import Lesson from '../views/Lesson.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/:moduleDir', name: 'module', component: Module },
    { path: '/:moduleDir/:lessonFile', name: 'lesson', component: Lesson },
  ],
})

export default router
