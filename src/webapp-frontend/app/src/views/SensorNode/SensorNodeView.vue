<template>
  <!-- Loading Animation -->
  <v-container v-if="loading" class="d-flex justify-center align-center" style="min-height: 300px">
    <v-progress-circular indeterminate color="primary" size="64" />
  </v-container>

  <v-container v-else>
    <v-row>
      <v-col cols="9">
        <!-- Sensor node Details -->
        <v-card class="mb-4" rounded="lg">
          <v-card-title>
            <v-row class="w-100 align-center">
                <!-- back button -->
                <v-col cols="auto">
                    <v-btn icon @click="router.back()">
                        <v-icon>mdi-arrow-left</v-icon>
                    </v-btn>
                </v-col>
                <!-- title -->
                <v-col>
                    <h2 class="mb-0">{{ sensorNode.name }}</h2>
                </v-col>
                <v-col cols="auto" class="d-flex align-center">
                  <!-- state-->
                  <v-chip
                  :color="sensorNode.state.color"
                  variant="flat"
                  class="me-2 text-white"
                  >
                    {{ sensorNode.state.label }}
                  </v-chip>
                  <!-- edit button -->
                  <v-btn
                  v-if="authStore.getUser?.role !== 'Researcher' && sensorNode.state.name !== 'unused'"
                  color="primary"
                  icon size="small"
                  class="me-1"
                  @click="router.push(`/sensor-node/${sensorNodeId}/edit`)"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <!-- delete button -->
                  <v-btn
                  v-if="authStore.getUser?.role !== 'Researcher' && sensorNode.state.name !== 'unused'"
                  color="error"
                  icon size="small"
                  @click="deletesensorNode(sensorNodeId)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-col>
            </v-row>
          </v-card-title>
          <v-divider class="my-6" />
          <!-- Sensor node content -->
          <v-card-text>
            <div class="mb-6">
              <h3 class="text-h6 mb-2">Notes</h3>
              <p class="text-body-1">{{ sensorNode.description }}</p>
            </div>
            <v-list elevation="1" rounded="lg" density="comfortable">
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-source-repository</v-icon>
                </template>
                <v-list-item-title>{{ sensorNode.gitlab_url }}</v-list-item-title>
                <v-list-item-subtitle>GitLab URL</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-source-branch</v-icon>
                </template>
                <v-list-item-title>{{ sensorNode.git_ref }}</v-list-item-title>
                <v-list-item-subtitle>Git Reference</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-chip</v-icon>
                </template>
                <v-list-item-title>{{ sensorNode.hardware_type }}</v-list-item-title>
                <v-list-item-subtitle>Hardware Type</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-identifier</v-icon>
                </template>
                <v-list-item-title>{{ sensorNode.uuid }}</v-list-item-title>
                <v-list-item-subtitle>UUID</v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <!-- configurables section -->
            <v-row class="mt-6">
            <v-col cols="6">
              <h3 class="text-h6 mb-2">Configurables</h3>
              <v-list elevation="1" rounded="lg" density="comfortable">
                <v-list-item
                  v-for="(config, index) in sensorNode.configurables"
                  :key="index"
                  style="min-height: 72px;"
                  :style="config.type === 'SystemDefined' ? 'background-color: rgba(0,0,0,0.05); font-style: italic;' : ''"
                >
                  <template #prepend>
                    <v-icon style="font-size: 28px;">mdi-cog</v-icon>
                  </template>
                    <v-list-item-title>{{config.name}}: <strong>{{ config.value }}</strong></v-list-item-title>
                </v-list-item>
              </v-list>
            </v-col>
            </v-row>
            <!-- Fields Table -->
            <h3 class="text-h6 mb-2 mt-6">Sensor node Fields</h3>
            <v-data-table
              :items="sensorNode.fields"
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
                :to="`/commercial-sensor/${item.commercial_sensor.uuid}`"
                style="text-transform: none; min-width: 150px;"
                
              >
                <v-icon start class="me-1">mdi-link-variant</v-icon>
                {{ item.commercial_sensor.alias }}
              </v-btn>
            </template>
            </v-data-table>

            <!-- protobuff schema -->
            <v-row class="align-center mb-2 mt-6">
              <v-col>
                <h3 class="text-h6 mb-0">Protobuf Schema</h3>
              </v-col>
              <v-col cols="auto">
                <v-btn
                  color="secondary"
                  size="small"
                  :href="`/sensor-node/${sensorNodeId}/code`"
                  download
                  style="text-transform: none;"
                >
                  <v-icon start class="me-1">mdi-download</v-icon>
                  Download Code
                </v-btn>
              </v-col>
            </v-row>
            <!-- <v-sheet
              elevation="1"
              class="pa-4 mt-4 position-relative"
              style="background-color: #272822; color: #f8f8f2; font-family: monospace; white-space: pre; overflow: auto; border-radius: 8px; max-height: 300px;"
            >
              <v-btn
                icon
                size="small"
                color="primary"
                @click="copySchema"
                class="position-absolute"
                style="top: 8px; right: 8px;"
              >
                <v-icon>mdi-content-copy</v-icon>
              </v-btn>
              {{ protobuf_schema }}
            </v-sheet> -->
          </v-card-text>
        </v-card>
        <v-divider class="my-6" />
        

        <h2 class="text-h6 mb-2">Deployed Nodes</h2>
        <!-- Table of deployed nodes
        <v-data-table
          :items="sensorNode.inherited_sensor_nodes"
          :headers="sensorHeaders"
          class="elevation-1 rounded-lg"
          hover
          density="compact"
          rounded="lg"
          elevation="1"
        >
          <template #item.state="{ item }">
            <v-chip :color="grey" variant="flat" class="text-white" style="min-width: 80px; justify-content: center;">
              {{ item.state }}
            </v-chip>
          </template>
        </v-data-table> -->
      </v-col>
      <!-- Logbook -->
      <v-col cols="3">
        <Logbook v-if="sensorNode?.logbook" :logbook="sensorNode.logbook" />
      </v-col>
    </v-row>
  </v-container>


  
  <!-- delete dialog -->
  <v-dialog v-model="confirmDelete" max-width="500">
    <v-card>
      <v-card-title class="text-h6">Confirm Deletion</v-card-title>
      <v-card-text>
        <p>To confirm deletion, type the sensor node name: <strong>{{ sensorNode?.name }}</strong></p>
        <v-text-field
          v-model="deleteConfirmInput"
          label="Sensor node name"
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
          :disabled="deleteConfirmInput !== sensorNode?.name"
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
import sensorNodeService from '@/services/sensorNodeService'
import Logbook from '@/components/Logbook.vue'
import { useAuthStore } from '@/stores/authStore'
import { useTextStore } from '@/stores/textStore'

const authStore = useAuthStore()
const textStore = useTextStore()
const sensorNodeId = ref(useRoute().params.id)
const router = useRouter()
const sensorNode = ref(null)

const sensorHeaders = [
  { title: 'Node ID', key: 'id' },
  { title: 'Name', key: 'name'},
  { title: 'Type', key: 'type' },
  { title: 'Location', key: 'location' },
  { title: 'State', key: 'state' },
]
const fieldHeaders = [
  { title: 'Field Name', key: 'field_name' },
  { title: 'Data Type', key: 'protbuf_datatype' },
  { title: 'Unit', key: 'unit' },
  { title: 'Commercial Sensor', key: 'commercial_sensor' },
]
const loading = ref(true)
const confirmDelete = ref(false)
const sensorNodeToDelete = ref(null)
const deleteConfirmInput = ref('')
const protobuf_schema = ref('')
// Fetch sensor node
sensorNodeService.getSensorNode(sensorNodeId.value)
  .then((data) => {
    sensorNode.value = data
    // Map the state property to an enum object definited in textstore that also contains a color and label value
    const matchedState = Object.values(textStore.sensorNodeStatusEnum).find(
      s => s.name === data.state
    )
    sensorNode.value.state = {
      name: data.state,
      label: matchedState ? matchedState.label : data.state,
      color: matchedState ? matchedState.color : 'grey'
    }
    console.log('sensor node', sensorNode.value)
  })
  .catch((error) => {
    console.error(`Error fetching sensor node ${sensorNodeId.value}:`, error)
  })
  .finally(() => loading.value = false)
// Fetch protobuff schema
// sensorNodeService.getSensorNodeSchema(sensorNodeId.value)
//   .then((data) => {
//     protobuf_schema.value = data
//   })
//   .catch((error) => {
//     console.error(`Error fetching sensor node ${sensorNodeId.value} schema:`, error)
//   })
// // check if the sensor node has children
// const hasInheritedSensorNodes = () => {
//   return Array.isArray(sensorNode.inherited_sensor_nodes) && sensorNode.inherited_sensor_nodes.length > 0
// }


const deletesensorNode = (id) => {
  sensorNodeToDelete.value = id
  deleteConfirmInput.value = ''
  confirmDelete.value = true
}

const performDelete = () => {
  sensorNodeService.deleteSensorNode(sensorNodeToDelete.value)
    .then(() => {
        confirmDelete.value = false
        router.push('/sensor-nodes')
    })
    .catch(() => console.error(`Error deleting sensor node ${sensorNodeToDelete.value}`))
}
const copySchema = () => {
  const schemaText = JSON.stringify(protobuf_schema.value, null, 2)
  navigator.clipboard.writeText(schemaText).catch(err => {
    console.error('Failed to copy schema: ', err)
  })
}


const latitude = 60.0
const longitude = 24.0
const zoom = 13

const mapUrl = `https://www.openstreetmap.org/export/embed.html?bbox=${longitude - 0.05}%2C${latitude - 0.05}%2C${longitude + 0.05}%2C${latitude + 0.05}&layer=mapnik&marker=${latitude}%2C${longitude}`

</script>