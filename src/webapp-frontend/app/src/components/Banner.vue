<template>
  <v-alert
    v-if="visible"
    :type="type"
    border="start"
    variant="tonal"
    :border-color="type"
    class="mb-4"
    style="position: relative;"
  >
    <div>{{ message }}</div>
    <div
      class="progress-bar"
      :style="{ width: progress + '%', position: 'absolute', bottom: '0', left: '0', height: '2px', backgroundColor: '#F7B232', transition: 'width 0.1s linear' }"
    />
  </v-alert>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import { useSettingsStore } from '@/stores/settingsStore'

const props = defineProps({
  message: { type: String, required: true },
  type: { type: String, default: 'info' },
  duration: { type: Number, default: useSettingsStore().bannerDuration }
})

const visible = ref(true)
const progress = ref(100)

const startTimer = () => {
  const start = performance.now()
  const end = start + props.duration

  const animate = (time) => {
    const remaining = end - time
    progress.value = Math.max((remaining / props.duration) * 100, 0)

    if (remaining > 0) {
      requestAnimationFrame(animate)
    } else {
      visible.value = false
    }
  }

  requestAnimationFrame(animate)
}

watchEffect(() => {
  visible.value = true
  startTimer()
})
</script>