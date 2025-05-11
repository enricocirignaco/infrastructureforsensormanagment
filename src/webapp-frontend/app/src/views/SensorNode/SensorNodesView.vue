<template>
  <v-container>
    <!-- Title & Button -->
    <v-row class="justify-space-between mb-4">
      <v-col cols="auto">
        <h1>Sensor Nodes</h1>
      </v-col>
    </v-row>
    <!-- Searchbar & state Filter -->
    <v-row class="align-center mb-4" dense>
      <v-col cols="12" class="d-flex align-center justify-space-between">
        <v-text-field
          v-model="tableSearch"
          label="Search sensor nodes"
          prepend-inner-icon="mdi-magnify"
          variant="solo-filled"
          hide-details
          density="compact"
          rounded
          style="max-width: 300px; "
          class="py-0"
        ></v-text-field>
        <div class="d-flex align-center" style="gap: 16px;">
          <v-switch
            v-model="hideInactive"
            label="Hide Inactive"
            inset
            hide-details
            density="comfortable"
            class="rounded-pill ma-0 pa-0"
            style="transform: scale(0.75); height: 28px;"
            color="secondary"
          ></v-switch>
          <v-switch
            v-model="hideArchived"
            label="Hide Archived"
            inset
            hide-details
            density="comfortable"
            class="rounded-pill ma-0 pa-0"
            style="transform: scale(0.75); height: 28px;"
            color="secondary"
          ></v-switch>
          <v-switch
            v-model="hidePrepared"
            label="Hide Prepared"
            inset
            hide-details
            density="comfortable"
            class="rounded-pill ma-0 pa-0"
            style="transform: scale(0.75); height: 28px;"
            color="secondary"
          ></v-switch>
        </div>
      </v-col>
    </v-row>
    <!-- Table -->
    <v-data-table
      :items="filteredSensorNodes"
      :headers="headers"
      v-model:search="tableSearch"
      @click:row="(_, { item }) => router.push(`/sensor-node/${item.uuid}`)"
      class="elevation-1 rounded-lg"
      hover
      rounded="lg"
      elevation="1"
      :loading="loading"
    >
      <template #item.state="{ item }">
        <v-chip :color="item.state.color" variant="flat" class="text-white" style="min-width: 80px; justify-content: center;">
          {{ item.state.label }}
        </v-chip>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTextStore } from '@/stores/textStore'
import sensorNodeService from '@/services/sensorNodeService'
import { computed } from 'vue'

const router = useRouter()
const textStore = useTextStore()
const sensorNodes = ref([])
const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Sensor Node ID', key: 'uuid' },
  { title: 'Project', key: 'project.name' },
  { title: 'Node Template', key: 'node_template.name' },
  { title: 'State', key: 'state'},
]
const loading = ref(true)
const tableSearch = ref('')
const hideInactive = ref(false)
const hideArchived = ref(false)
const hidePrepared = ref(false)

// Filter entries based on toggle buttons state
const filteredSensorNodes = computed(() => {
  return sensorNodes.value.filter(item => {
    if (hideArchived.value && item.state.name === 'Archived') return false
    if (hideInactive.value && item.state.name === 'Inactive') return false
    if (hidePrepared.value && item.state.name === 'Prepared') return false
    return true
  })
})
// Fetch sensor node data
sensorNodeService.getSensorNodesDTO()
  .then((data) => {
    // Map the state property to an enum object definited in textstore that also contains a color and label value
    sensorNodes.value = data.map(item => {
      const matched = Object.values(textStore.sensorNodeStatusEnum).find(
        s => s.name === item.state
      )
      return {
        ...item,
        state: {
          name: item.state,
          label: matched ? matched.label : item.state,
          color: matched ? matched.color : 'grey'
        }
      }
  })
  })
  .catch((error) => {
    console.error('Error fetching sensor nodes:', error)
  })
  .finally(() => loading.value = false)
</script>
