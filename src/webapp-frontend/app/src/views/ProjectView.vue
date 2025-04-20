<template>
  <v-container>
    <!-- Project Details -->
    <v-card class="mb-4" rounded="lg">
      <v-card-title>
        <v-row class="w-100 align-center">
          <v-col cols="auto">
            <v-btn icon @click="$router.back()">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
          </v-col>
          <v-col>
            <h2 class="mb-0">{{ project.name }} - {{ project.short_name }}</h2>
          </v-col>
          <v-col cols="auto">
            <v-chip color="primary" variant="flat">{{ project.state }}</v-chip>
          </v-col>
        </v-row>
      </v-card-title>
      <v-divider class="my-6" />

      <v-card-text>
        <div class="mb-6">
          <h3 class="text-h6 mb-2">Project Description</h3>
          <p class="text-body-1">{{ project.description }}</p>
        </div>
        <h3 class="text-h6 mb-2">Project Resources</h3>
        <v-data-table
          :headers="[
            { title: 'Name', key: 'name' },
            { title: 'Type', key: 'type' },
            { title: 'URL', key: 'url' }
          ]"
          :items="project.external_props"
          density="compact"
          class="rounded-lg elevation-1"
          hide-default-footer
        >
          <template #item.url="{ item }">
            <a :href="item.url" target="_blank">{{ item.url }}</a>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
    <v-divider class="my-6" />

    <h2 class="text-h6 mb-2">Deployed Nodes</h2>
    <!-- Table -->
    <v-data-table
      :items="projects"
      :headers="headers"
      @click:row="(_, { item }) => router.push(`/projects/${item.id}`)"
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

const project = ref({
  name: 'Internet of Soils',
  short_name: 'IoS',
  description: 'A research project focused on soil monitoring using IoT sensors.',
  external_props: [
    { name: 'GitHub Repository', url: 'https://github.com/example/internet-of-soils', type: 'Repository' },
    { name: 'Project Website', url: 'https://internetofsoils.example.org', type: 'Website' }
  ],
  state: 'Active'
})

const sensorHeaders = [
  { title: 'Node ID', key: 'id' },
  { title: 'Location', key: 'location' },
  { title: 'Status', key: 'status' },
]

const sensorNodes = ref([
  { id: 'node-01', location: 'Field A', status: 'Online' },
  { id: 'node-02', location: 'Field B', status: 'Offline' },
  { id: 'node-03', location: 'Greenhouse', status: 'Online' },
])
</script>