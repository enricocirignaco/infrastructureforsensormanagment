<template>
  <v-card class="pa-4" elevation="2" rounded="lg">
    <v-card-title class="text-h6">Logbook</v-card-title>

    <v-divider class="my-4" />

    <v-card-subtitle class="text-subtitle-1">Last Edited</v-card-subtitle>
    <v-list dense>
      <v-list-item v-for="(entry, index) in updatedAtEntries" :key="index">
        <div>
          <strong>{{ entry.user.full_name }}</strong>
          <br />
          <small>
            {{
              new Date(entry.date).toLocaleDateString() +
              ' — ' +
              new Date(entry.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            }}
          </small>
        </div>
      </v-list-item>
    </v-list>

    <v-divider class="my-4" />

    <v-card-subtitle class="text-subtitle-1">Created</v-card-subtitle>
    <v-list dense>
      <v-list-item v-if="createdAtEntry">
        <div>
          <strong>{{ createdAtEntry.user.full_name }}</strong>
          <br />
          <small>{{
              new Date(createdAtEntry.date).toLocaleDateString() +
              ' — ' +
              new Date(createdAtEntry.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            }}</small>
        </div>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
// defineProps of the component
const { logbook } = defineProps({
  logbook: {
    type: Array,
    default: () => []
  }
})
const updatedAtEntries = computed(() =>
  (logbook || []).filter(entry => entry.type === 'Updated')
)

const createdAtEntry = computed(() =>
  (logbook || []).find(entry => entry.type === 'Created') || null
)
</script>