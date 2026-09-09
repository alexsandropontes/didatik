<script setup>
import { computed, ref, watchEffect, onMounted, onBeforeUnmount, useTemplateRef } from 'vue'
import { useRoute } from 'vue-router'
import { unified } from 'unified'
import remarkParse from 'remark-parse'
import remarkGfm from 'remark-gfm'
import remarkRehype from 'remark-rehype'
import rehypeRaw from 'rehype-raw'
import rehypeSlug from 'rehype-slug'
import rehypeStringify from 'rehype-stringify'
import { getCourse, getLesson, splitLrf, parseQuiz } from '../utils/courseLoader'
import { useProgress } from '../composables/useProgress'
import QuizSection from '../components/QuizSection.vue'

const processor = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkRehype, { allowDangerousHtml: true })
  .use(rehypeRaw)
  .use(rehypeSlug)
  .use(rehypeStringify)

const route = useRoute()
const course = computed(() => getCourse(route.params.courseSlug))
const lesson = computed(() =>
  course.value
    ? getLesson(course.value.slug, route.params.moduleDir, route.params.lessonFile)
    : null
)
const html = ref({ learn: '', run: '', fly: '' })
const quiz = ref(null)

const { isCompleted, getScore, markCompleted, moduleStats } = useProgress()
const completed = ref(false)
const savedScore = ref(null)

// Status do módulo (reativo ao progresso) — exibido após passar no quiz
const modStats = computed(() =>
  course.value && lesson.value
    ? moduleStats(course.value.slug, lesson.value.module)
    : { done: 0, total: 0, pct: 0 }
)
const moduleFinished = computed(
  () => completed.value && modStats.value.total > 0 && modStats.value.done === modStats.value.total
)

const nextModule = computed(() => {
  if (!course.value || !lesson.value) return null
  const idx = course.value.modules.findIndex((m) => m.dir === lesson.value.moduleDir)
  return idx >= 0 ? course.value.modules[idx + 1] || null : null
})

watchEffect(async () => {
  if (!lesson.value) return
  const sections = splitLrf(lesson.value.body)
  quiz.value = parseQuiz(sections.quiz)
  const rendered = {}
  for (const key of ['learn', 'run', 'fly']) {
    rendered[key] = await processor.process(sections[key] || '')
  }
  html.value = {
    learn: String(rendered.learn),
    run: String(rendered.run),
    fly: String(rendered.fly),
  }
  completed.value = isCompleted(course.value.slug, lesson.value.moduleDir, lesson.value.slug)
  savedScore.value = getScore(course.value.slug, lesson.value.moduleDir, lesson.value.slug)
})

function onQuizPassed(score) {
  if (course.value && lesson.value) {
    markCompleted(course.value.slug, lesson.value.moduleDir, lesson.value.slug, score)
    completed.value = true
    savedScore.value = score
  }
}

// Fase LRF ativa conforme a leitura (scroll)
const activePhase = ref('learn')
const learnEl = useTemplateRef('learnSection')
const runEl = useTemplateRef('runSection')
const flyEl = useTemplateRef('flySection')
let observer = null

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          activePhase.value = entry.target.dataset.phase
        }
      }
    },
    { rootMargin: '-30% 0px -55% 0px' }
  )
  for (const el of [learnEl.value, runEl.value, flyEl.value]) {
    if (el) observer.observe(el)
  }
})

onBeforeUnmount(() => observer?.disconnect())

function scrollToPhase(phase) {
  const map = { learn: learnEl, run: runEl, fly: flyEl }
  map[phase]?.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<template>
  <article v-if="lesson && course" class="lesson">
    <nav class="lesson-nav-top">
      <RouterLink to="/">Cursos</RouterLink>
      <span class="crumb-sep">›</span>
      <RouterLink :to="`/${course.slug}`">{{ course.title }}</RouterLink>
      <span class="crumb-sep">›</span>
      <RouterLink :to="`/${course.slug}/${lesson.module.dir}`">
        {{ lesson.module.title }}
      </RouterLink>
    </nav>

    <header class="lesson-header">
      <span class="crumb">
        Módulo {{ String(lesson.module.order).padStart(2, '0') }} · Aula
        {{ String(lesson.order).padStart(2, '0') }}
      </span>
      <h1>
        {{ lesson.title }}
        <span v-if="completed" class="done-badge" title="Aula concluída">✅</span>
      </h1>
      <p v-if="completed" class="done-note">
        Aula concluída com {{ savedScore }}% de aproveitamento. 🚀
      </p>
      <div class="tags" v-if="lesson.tags.length">
        <span v-for="tag in lesson.tags" :key="tag" class="tag">#{{ tag }}</span>
      </div>
    </header>

    <nav class="lrf-progress" aria-label="Progresso da aula">
      <a
        href="#learn"
        class="phase"
        data-phase="learn"
        :data-active="activePhase === 'learn'"
        @click.prevent="scrollToPhase('learn')"
      >🧠 Learn</a>
      <span class="phase-line">─</span>
      <a
        href="#run"
        class="phase"
        data-phase="run"
        :data-active="activePhase === 'run'"
        @click.prevent="scrollToPhase('run')"
      >🏃 Run</a>
      <span class="phase-line">─</span>
      <a
        href="#fly"
        class="phase"
        data-phase="fly"
        :data-active="activePhase === 'fly'"
        @click.prevent="scrollToPhase('fly')"
      >🚀 Fly</a>
    </nav>

    <section ref="learnSection" class="lrf-section learn" data-phase="learn">
      <h2>🧠 Learn</h2>
      <div class="markdown" v-html="html.learn"></div>
    </section>

    <section ref="runSection" class="lrf-section run" data-phase="run">
      <h2>🏃 Run</h2>
      <div class="markdown" v-html="html.run"></div>
    </section>

    <section ref="flySection" class="lrf-section fly" data-phase="fly">
      <h2>🚀 Fly</h2>
      <div class="markdown" v-html="html.fly"></div>
    </section>

    <QuizSection
      v-if="quiz"
      :questions="quiz"
      @passed="onQuizPassed"
    />

    <div v-if="completed" class="module-feedback" :class="moduleFinished ? 'finished' : 'partial'">
      <template v-if="moduleFinished">
        <p class="feedback-title">🏆 Módulo concluído!</p>
        <p>
          Você finalizou todas as {{ modStats.total }} aulas de
          <strong>{{ lesson.module.title }}</strong>. Nota nesta aula:
          <strong>{{ savedScore }}%</strong>.
        </p>
        <RouterLink v-if="nextModule" :to="`/${course.slug}/${nextModule.dir}`" class="feedback-cta">
          Próximo módulo: {{ nextModule.title }} →
        </RouterLink>
        <RouterLink v-else :to="`/${course.slug}`" class="feedback-cta">
          🎓 Curso concluído! Voltar ao início →
        </RouterLink>
      </template>
      <template v-else>
        <p class="feedback-title">✅ Aula concluída! ({{ savedScore }}%)</p>
        <p>
          Progresso do módulo <strong>{{ lesson.module.title }}</strong>:
          {{ modStats.done }}/{{ modStats.total }} aulas ({{ modStats.pct }}%).
        </p>
        <RouterLink
          v-if="lesson.next"
          :to="`/${course.slug}/${lesson.module.dir}/${lesson.next.slug}`"
          class="feedback-cta"
        >
          Continuar: {{ lesson.next.title }} →
        </RouterLink>
      </template>
    </div>

    <nav class="lesson-nav-bottom">
      <RouterLink
        v-if="lesson.prev"
        :to="`/${course.slug}/${lesson.module.dir}/${lesson.prev.slug}`"
        class="nav-prev"
      >
        <span class="nav-label">← Aula anterior</span>
        {{ lesson.prev.title }}
      </RouterLink>
      <span v-else></span>
      <RouterLink
        v-if="lesson.next"
        :to="`/${course.slug}/${lesson.module.dir}/${lesson.next.slug}`"
        class="nav-next"
      >
        <span class="nav-label">Próxima aula →</span>
        {{ lesson.next.title }}
      </RouterLink>
    </nav>
  </article>
  <section v-else class="empty">Aula não encontrada. 😕</section>
</template>
