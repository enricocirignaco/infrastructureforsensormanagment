<template>
  <!-- Loading Animation -->
  <v-container v-if="loading" class="d-flex justify-center align-center" style="min-height: 300px">
    <v-progress-circular indeterminate color="primary" size="64" />
  </v-container>
  <v-container v-else>
    <v-row>
      <v-col cols="9">
        <!-- Node Template Details -->
        <v-card class="mb-4" rounded="lg">
          <v-card-title>
            <v-row class="w-100 align-center">
                <!-- back button -->
                <v-col cols="auto">
                    <v-btn icon @click="router.push('/node-templates')">
                        <v-icon>mdi-arrow-left</v-icon>
                    </v-btn>
                </v-col>
                <!-- title -->
                <v-col>
                    <h2 class="mb-0">{{ nodeTemplate.name }}</h2>
                </v-col>
                <v-col cols="auto" class="d-flex align-center">
                  <!-- status-->
                  <v-chip
                  :color="nodeTemplate.status.color"
                  variant="flat"
                  class="me-2 text-white"
                  >
                    {{ nodeTemplate.status.label }}
                  </v-chip>
                  <!-- edit button -->
                  <v-btn
                  v-if="authStore.getUser?.role !== 'Researcher' && !hasInheritedSensorNodes()"
                  color="primary"
                  icon size="small"
                  class="me-1"
                  @click="router.push(`/node-template/${nodeTemplateId}/edit`)"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <!-- delete button -->
                  <v-btn
                  v-if="authStore.getUser?.role !== 'Researcher' && !hasInheritedSensorNodes()"
                  color="error"
                  icon size="small"
                  @click="deleteProject(nodeTemplateId)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-col>
            </v-row>
          </v-card-title>
          <v-divider class="my-6" />
          <!-- Node Template content -->
          <v-card-text>
            <div class="mb-6">
              <h3 class="text-h6 mb-2">Node Template Description</h3>
              <p class="text-body-1">{{ nodeTemplate.description }}</p>
            </div>
            <v-list elevation="1" rounded="lg" density="comfortable">
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-source-repository</v-icon>
                </template>
                <v-list-item-title>{{ nodeTemplate.gitlab_url }}</v-list-item-title>
                <v-list-item-subtitle>GitLab URL</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-source-branch</v-icon>
                </template>
                <v-list-item-title>{{ nodeTemplate.git_ref }}</v-list-item-title>
                <v-list-item-subtitle>Git Reference</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-chip</v-icon>
                </template>
                <v-list-item-title>{{ nodeTemplate.hardware_type }}</v-list-item-title>
                <v-list-item-subtitle>Hardware Type</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-identifier</v-icon>
                </template>
                <v-list-item-title>{{ nodeTemplate.uuid }}</v-list-item-title>
                <v-list-item-subtitle>UUID</v-list-item-subtitle>
              </v-list-item>

            </v-list>

            <!-- Fields Table -->
            <h3 class="text-h6 mb-2 mt-6">Node Template Fields</h3>
            <v-data-table
              :items="nodeTemplate.fields"
              :headers="fieldHeaders"
              density="compact"
              class="elevation-1 rounded-lg"
              hide-default-footer
              rounded="lg"
              elevation="1"
              disable-sort
            >
            <template #item.commercial_sensor="{ item }">
              <v-btn
                variant="outlined"
                color="secondary"
                size="small"
                rounded
                :to="`/commercial-sensor/${item.commercial_sensor}`"
                style="text-transform: none;"
              >
                <v-icon start class="me-1">mdi-link-variant</v-icon>
                View Sensor
              </v-btn>
            </template>
            </v-data-table>

            <!-- protobuff schema to copy -->
            <h3 class="text-h6 mb-2 mt-6">Protobuf Schema</h3>           
            <v-sheet
              elevation="1"
              class="pa-4 mt-4"
              style="background-color: #272822; color: #f8f8f2; font-family: monospace; white-space: pre; overflow-x: auto; border-radius: 8px;"
            >
            
              {{ nodeTemplate.protobuf_schema }}
            </v-sheet>
            
          </v-card-text>


        </v-card>
        <v-divider class="my-6" />
        

        <h2 class="text-h6 mb-2">Deployed Nodes</h2>
        <!-- Table of deployed nodes -->
        <v-data-table
          :items="nodeTemplate.sensor_nodes"
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
      </v-col>
      <!-- Logbook -->
      <v-col cols="3">
        <Logbook v-if="nodeTemplate?.logbook" :logbook="nodeTemplate.logbook" />
      </v-col>
    </v-row>
  </v-container>


  
  <!-- delete dialog -->
  <v-dialog v-model="confirmDelete" max-width="500">
    <v-card>
      <v-card-title class="text-h6">Confirm Deletion</v-card-title>
      <v-card-text>
        <p>To confirm deletion, type the project name: <strong>{{ nodeTemplate?.name }}</strong></p>
        <v-text-field
          v-model="deleteConfirmInput"
          label="Project name"
          dense
          hide-details
          autofocus
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="confirmDelete = false">Cancel</v-btn>
        <v-btn
          color="error"
          text
          :disabled="deleteConfirmInput !== nodeTemplate?.name"
          @click="performDelete"
        >
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import nodeTemplateService from '@/services/nodeTemplateService'
import Logbook from '@/components/Logbook.vue'
import { useAuthStore } from '@/stores/authStore'
import { useTextStore } from '@/stores/textStore'

const authStore = useAuthStore()
const textStore = useTextStore()
const nodeTemplateId = ref(useRoute().params.id)
const router = useRouter()
const nodeTemplate = ref(null)
const nodeTemplateHeaders = [
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
const fieldHeaders = [
  { title: 'Field Name', key: 'field_name' },
  { title: 'Data Type', key: 'protbuf_datatype' },
  { title: 'Unit', key: 'unit' },
  { title: 'Commercial Sensor', key: 'commercial_sensor' },
]
const groupBy = ref([{ key: 'type', order: 'asc' }])
const loading = ref(true)
const confirmDelete = ref(false)
const nodeTemplateToDelete = ref(null)
const deleteConfirmInput = ref('')

// Fetch node template
nodeTemplateService.getNodeTemplate(nodeTemplateId.value)
  .then((data) => {
    nodeTemplate.value = data
    // Map the status property to an enum object definited in textstore that also contains a color and label value
    const matchedStatus = Object.values(textStore.nodeTemplateStatusEnum).find(
      s => s.name === data.status
    )
    nodeTemplate.value.status = {
      name: data.status,
      label: matchedStatus ? matchedStatus.label : data.status,
      color: matchedStatus ? matchedStatus.color : 'grey'
    }
  })
  .catch((error) => {
    console.error(`Error fetching node template ${nodeTemplateId.value}:`, error)
  })
  .finally(() => loading.value = false)

const hasInheritedSensorNodes = () => {
  return Array.isArray(nodeTemplate.inherited_sensor_nodes) && nodeTemplate.inherited_sensor_nodes.length > 0
}
const deleteProject = (id) => {
  nodeTemplateToDelete.value = id
  deleteConfirmInput.value = ''
  confirmDelete.value = true
}

// const performDelete = () => {
//   projectService.deleteProject(projectToDelete.value)
//     .then(() => {
//         confirmDelete.value = false
//         router.push('/projects')
//     })
//     .catch(() => console.error(`Error deleting project ${projectToDelete.value}`))
// }
const copySchema = () => {
  navigator.clipboard.writeText(nodeTemplate.value.protobuf_schema).then(() => {
    console.log('Schema copied to clipboard!')
  }).catch(err => {
    console.error('Failed to copy schema:', err)
  })
}
</script>