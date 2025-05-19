<template>
  <v-container>
    <!-- Title & Button -->
    <v-row class="justify-space-between mb-4">
      <v-col cols="auto">
        <h1>Projects</h1>
      </v-col>
      <v-col cols="auto">
      <v-btn v-if="authStore.getUser?.role !== 'Researcher'" rounded="xl" class="text-none" @click="router.push('/project/new')">
        <v-icon start>mdi-plus</v-icon>
        New Project
      </v-btn>
      </v-col>
    </v-row>
    <!-- Table -->
    <v-data-table
      :items="projects"
      :headers="headers"
      @click:row="(_, { item }) => router.push(`/project/${item.uuid}`)"
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
import projectService from '@/services/projectService'
import { useAuthStore } from '@/stores/authStore'
import { useTextStore } from '@/stores/textStore'

const textStore = useTextStore()
const authStore = useAuthStore()
const router = useRouter()
const projects = ref([])
const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Short Name', key: 'short_name' },
  { title: 'Project ID', key: 'uuid' },
  { title: 'State', key: 'state' },
]
const loading = ref(true)
// Fetch projects data
projectService.getProjectsDTO()
  .then((data) => {
    projects.value = data

    // Map the state property to an enum object definited in textstore that also contains a color and label value
    projects.value = data.map(item => {
      const matched = Object.values(textStore.projectStatusEnum).find(
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
    console.error('Error fetching projects:', error)
  })
  .finally(() => loading.value = false)
</script>
