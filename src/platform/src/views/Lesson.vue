<script setup>
import { computed, ref, watchEffect } from 'vue'
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

    <div class="lrf-progress">
      <span class="phase active" data-phase="learn">🧠 Learn</span>
      <span class="phase-line">─</span>
      <span class="phase" data-phase="run">🏃 Run</span>
      <span class="phase-line">─</span>
      <span class="phase" data-phase="fly">🚀 Fly</span>
    </div>

    <section class="lrf-section learn">
      <h2>🧠 Learn</h2>
      <div class="markdown" v-html="html.learn"></div>
    </section>

    <section class="lrf-section run">
      <h2>🏃 Run</h2>
      <div class="markdown" v-html="html.run"></div>
    </section>

    <section class="lrf-section fly">
      <h2>🚀 Fly</h2>
      <div class="markdown" v-html="html.fly"></div>
    </section>

    <nav class="lesson-nav-bottom">
      <RouterLink
        v-if="lesson.prev"
        :to="`/${lesson.module.dir}/${lesson.prev.slug}`"
        class="nav-prev"
      >
        ← {{ lesson.prev.title }}
      </RouterLink>
      <span v-else></span>
      <RouterLink
        v-if="lesson.next"
        :to="`/${lesson.module.dir}/${lesson.next.slug}`"
        class="nav-next"
      >
        {{ lesson.next.title }} →
      </RouterLink>
    </nav>
  </article>
  <section v-else class="empty">Aula não encontrada. 😕</section>
</template>
