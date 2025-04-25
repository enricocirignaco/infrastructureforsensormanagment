<template>
  <v-container>
    <!-- Title & Button -->
    <v-row class="justify-space-between mb-4">
      <v-col cols="auto">
        <h1>Projects</h1>
      </v-col>
      <v-col cols="auto">
      <v-btn rounded="xl" class="text-none" @click="router.push('/project/new')">
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
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import projectService from '@/services/projectService'

const router = useRouter()
const projects = ref([])
const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Short Name', key: 'short_name' },
  { title: 'Status', key: 'state' },
  { title: 'Project ID', key: 'uuid' }
]
const loading = ref(true)
// Fetch projects data
projectService.getProjectsDTO()
  .then((data) => projects.value = data)
  .catch((error) => {
    // TODO: Handle error
    console.error('Error fetching projects:', error)
  })
  .finally(() => loading.value = false)
</script>
