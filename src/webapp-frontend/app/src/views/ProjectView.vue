<template>
  <v-container v-if="loading" class="d-flex justify-center align-center" style="min-height: 300px">
    <v-progress-circular indeterminate color="primary" size="64" />
  </v-container>
  <v-container v-else>
    <!-- Project Details -->
    <v-card class="mb-4" rounded="lg">
      <v-card-title>
        <v-row class="w-100 align-center">
            <!-- back button -->
            <v-col cols="auto">
                <v-btn icon @click="$router.back()">
                <v-icon>mdi-arrow-left</v-icon>
                </v-btn>
            </v-col>
            <!-- title -->
            <v-col>
                <h2 class="mb-0">{{ project.name }} - {{ project.short_name }}</h2>
            </v-col>
            <!-- status & edit button -->
            <v-col cols="auto" class="d-flex align-center">
                <v-chip :color="getStatusColor(project.state)" variant="flat" class="me-2 text-white">
                  {{ project.state }}
                </v-chip>
                <v-btn color="primary" icon size="small" @click="router.push(`/project/${projectId}/edit`)">
                    <v-icon>mdi-pencil</v-icon>
                </v-btn>
            </v-col>
        </v-row>
      </v-card-title>
      <v-divider class="my-6" />
      <!-- Project content -->
      <v-card-text>
        <div class="mb-6">
          <h3 class="text-h6 mb-2">Project Description</h3>
          <p class="text-body-1">{{ project.description }}</p>
        </div>
        <h3 class="text-h6 mb-2">Project Resources</h3>
        <v-data-table
          :items="project.external_props"
          :headers="projectHeaders"
          density="compact"
          class="rounded-lg elevation-1"
          hide-default-footer
          :group-by="groupBy"
          rounded="lg"
          elevation="1"
          show-group-by
        >
          <template #item.url="{ item }">
            <a :href="item.url" target="_blank">{{ item.url }}</a>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
    <v-divider class="my-6" />

    <h2 class="text-h6 mb-2">Deployed Nodes</h2>
    <!-- Table of deployed nodes -->
    <v-data-table
      :items="project.sensor_nodes"
      :headers="sensorHeaders"
      class="elevation-1 rounded-lg"
      hover
      density="compact"
      rounded="lg"
      elevation="1"
    >
      <template #item.status="{ item }">
        <v-chip :color="getStatusColor(item.status)" variant="flat" class="text-white" style="min-width: 80px; justify-content: center;">
          {{ item.status }}
        </v-chip>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import projectService from '@/services/projectService'

const projectId = ref(useRoute().params.id)
const router = useRouter()
const project = ref(null)
const projectHeaders = [
    { title: 'Name', key: 'name' },
    { title: 'URL', key: 'url' }
]
const sensorHeaders = [
  { title: 'Node ID', key: 'id' },
  { title: 'Name', key: 'name'},
  { title: 'Type', key: 'type' },
  { title: 'Location', key: 'location' },
  { title: 'Status', key: 'status' },
]
const groupBy = ref([{ key: 'type', order: 'asc' }])
const loading = ref(true)
// Fetch project data
projectService.getProject(projectId.value)
    .then((data) => project.value = data)
    .catch((error) => {
    // TODO: Handle error
    console.error(`Error fetching project ${projectId.value}:`, error)
  })
  .finally(() => loading.value = false)
// render status color
function getStatusColor (status) {
    if (status === 'Active') return 'success'
    else if (status === 'Inactive') return 'warning'
    else if (status === 'Error') return 'error'
    else return 'grey'
  }
const editStatus = () => {
  console.log('Edit status clicked')
}
</script>