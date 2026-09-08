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
import { getLesson, splitLrf } from '../utils/courseLoader'

const processor = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkRehype, { allowDangerousHtml: true })
  .use(rehypeRaw)
  .use(rehypeSlug)
  .use(rehypeStringify)

const route = useRoute()
const lesson = computed(() => getLesson(route.params.moduleDir, route.params.lessonFile))
const html = ref({ learn: '', run: '', fly: '' })

watchEffect(async () => {
  if (!lesson.value) return
  const sections = splitLrf(lesson.value.body)
  const rendered = {}
  for (const key of ['learn', 'run', 'fly']) {
    rendered[key] = await processor.process(sections[key] || '')
  }
  html.value = {
    learn: String(rendered.learn),
    run: String(rendered.run),
    fly: String(rendered.fly),
  }
})

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
  <article v-if="lesson" class="lesson">
    <nav class="lesson-nav-top">
      <RouterLink :to="`/${lesson.module.dir}`">
        ← {{ lesson.module.title }}
      </RouterLink>
    </nav>

    <header class="lesson-header">
      <span class="crumb">
        Módulo {{ String(lesson.module.order).padStart(2, '0') }} · Aula
        {{ String(lesson.order).padStart(2, '0') }}
      </span>
      <h1>{{ lesson.title }}</h1>
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

    <nav class="lesson-nav-bottom">
      <RouterLink
        v-if="lesson.prev"
        :to="`/${lesson.module.dir}/${lesson.prev.slug}`"
        class="nav-prev"
      >
        <span class="nav-label">← Aula anterior</span>
        {{ lesson.prev.title }}
      </RouterLink>
      <span v-else></span>
      <RouterLink
        v-if="lesson.next"
        :to="`/${lesson.module.dir}/${lesson.next.slug}`"
        class="nav-next"
      >
        <span class="nav-label">Próxima aula →</span>
        {{ lesson.next.title }}
      </RouterLink>
    </nav>
  </article>
  <section v-else class="empty">Aula não encontrada. 😕</section>
</template>
