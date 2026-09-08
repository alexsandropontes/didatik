<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  questions: { type: Array, required: true },
  passingScore: { type: Number, default: 75 },
})

const emit = defineEmits(['passed'])

const answers = ref({})
const submitted = ref(false)
const lastScore = ref(null)

const allAnswered = computed(() =>
  props.questions.every((_, i) => answers.value[i] !== undefined)
)

const score = computed(() => {
  if (!submitted.value) return null
  const correct = props.questions.filter((q, i) => answers.value[i] === q.answer).length
  return Math.round((correct / props.questions.length) * 100)
})

const passed = computed(() => submitted.value && score.value >= props.passingScore)

function submit() {
  submitted.value = true
  lastScore.value = score.value
  if (passed.value) emit('passed', score.value)
}

function retry() {
  submitted.value = false
  answers.value = {}
}
</script>

<template>
  <section class="lrf-section quiz">
    <h2>📝 Quiz</h2>
    <p class="quiz-hint">
      Acerte pelo menos <strong>{{ passingScore }}%</strong> para concluir a aula.
    </p>

    <div v-for="(q, qi) in questions" :key="qi" class="quiz-question">
      <p class="quiz-prompt">{{ qi + 1 }}. {{ q.prompt }}</p>
      <label
        v-for="(opt, oi) in q.options"
        :key="oi"
        class="quiz-option"
        :class="{
          selected: answers[qi] === oi,
          correct: submitted && oi === q.answer,
          wrong: submitted && answers[qi] === oi && oi !== q.answer,
        }"
      >
        <input
          type="radio"
          :name="`q-${qi}`"
          :value="oi"
          :disabled="submitted"
          v-model="answers[qi]"
        />
        <span>{{ opt }}</span>
      </label>
    </div>

    <div class="quiz-actions">
      <button v-if="!submitted" class="quiz-btn" :disabled="!allAnswered" @click="submit">
        Verificar respostas
      </button>
      <button v-else class="quiz-btn secondary" @click="retry">Refazer quiz</button>
    </div>

    <div v-if="submitted" class="quiz-result" :class="passed ? 'passed' : 'failed'">
      <template v-if="passed">
        🎉 <strong>{{ score }}%</strong> — aproveitamento suficiente. Aula concluída!
      </template>
      <template v-else>
        😕 <strong>{{ score }}%</strong> — precisa de {{ passingScore }}% para concluir.
        Revise o Learn e tente de novo!
      </template>
    </div>
  </section>
</template>
