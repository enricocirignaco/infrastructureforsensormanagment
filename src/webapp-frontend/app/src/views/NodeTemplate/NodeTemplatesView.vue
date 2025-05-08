<template>
  <v-container>
    <!-- Title & Button -->
    <v-row class="justify-space-between mb-4">
      <v-col cols="auto">
        <h1>Node Templates</h1>
      </v-col>
      <v-col cols="auto">
      <v-btn v-if="authStore.getUser?.role !== 'Researcher'" rounded="xl" class="text-none" @click="router.push('/node-template/new')">
        <v-icon start>mdi-plus</v-icon>
        New Node Template
      </v-btn>
      </v-col>
    </v-row>
    <!-- Searchbar & status Filter -->
    <v-row class="align-center mb-4" dense>
      <v-col cols="12" class="d-flex align-center justify-space-between">
        <v-text-field
          v-model="tableSearch"
          label="Search node templates"
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
            v-model="hideUnused"
            label="Hide Unused"
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
      :items="filteredNodeTemplates"
      :headers="headers"
      v-model:search="tableSearch"
      @click:row="(_, { item }) => router.push(`/node-template/${item.uuid}`)"
      class="elevation-1 rounded-lg"
      hover
      rounded="lg"
      elevation="1"
      :loading="loading"
    >
      <template #item.status="{ item }">
        <v-chip :color="item.status.color" variant="flat" class="text-white" style="min-width: 80px; justify-content: center;">
          {{ item.status.label }}
        </v-chip>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useTextStore } from '@/stores/textStore'
import nodeTemplateService from '@/services/nodeTemplateService'
import { computed } from 'vue'

const authStore = useAuthStore()
const router = useRouter()
const textStore = useTextStore()
const nodeTemplates = ref([])
const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Hardware Type', key: 'hardware_type' },
  { title: 'Node Template ID', key: 'uuid' },
  { title: 'Status', key: 'status'},
]
const loading = ref(true)
const tableSearch = ref('')
const hideUnused = ref(false)
const hideArchived = ref(false)

// Filter entries based on toggle buttons state
const filteredNodeTemplates = computed(() => {
  return nodeTemplates.value.filter(item => {
    if (hideArchived.value && item.status.name === 'archived') return false
    if (hideUnused.value && item.status.name === 'unused') return false
    return true
  })
})
// Fetch projects data
nodeTemplateService.getNodeTemplatesDTO()
  .then((data) => {
    // Map the status property to an enum object definited in textstore that also contains a color and label value
    nodeTemplates.value = data.map(item => {
      const matched = Object.values(textStore.nodeTemplateStatusEnum).find(
        s => s.name === item.status
      )
      return {
        ...item,
        status: {
          name: item.status,
          label: matched ? matched.label : item.status,
          color: matched ? matched.color : 'grey'
        }
      }
  })
  })

  .catch((error) => {
    console.error('Error fetching projects:', error)
  })
  .finally(() => loading.value = false)
</script>
