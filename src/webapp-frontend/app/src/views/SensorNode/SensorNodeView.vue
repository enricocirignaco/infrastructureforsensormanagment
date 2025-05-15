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
                    <v-btn icon @click="router.push('/sensor-nodes')">
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
                  v-if="authStore.getUser?.role !== 'Researcher'"
                  color="primary"
                  icon size="small"
                  class="me-1"
                  @click="router.push(`/sensor-node/${sensorNodeId}/edit`)"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <!-- delete button -->
                  <v-btn
                  v-if="authStore.getUser?.role !== 'Researcher' && sensorNode.state.name === 'Prepared'"
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
              <v-list-item
              style="min-height: 72px; cursor: pointer;"
              @click="openTTNUrl"
              >
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-web</v-icon>
                </template>
                <v-list-item-title>{{ sensorNode.ttn_device_link }}</v-list-item-title>
                <v-list-item-subtitle>The Things Network URL</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item
              style="min-height: 72px; cursor: pointer;"
              @click="router.push(`/project/${sensorNode.project_uuid}`)"
              >
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-forest</v-icon>
                </template>
                <v-list-item-title>{{ sensorNode.project_uuid }}</v-list-item-title>
                <v-list-item-subtitle>Project UUID</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item
              style="min-height: 72px; cursor: pointer;"
              @click="router.push(`/node-template/${sensorNode.node_template_uuid}`)"
              >
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-file-document-multiple</v-icon>
                </template>
                <v-list-item-title>{{ sensorNode.node_template_uuid }}</v-list-item-title>
                <v-list-item-subtitle>Node Template UUID</v-list-item-subtitle>
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
            <v-divider class="my-6" />
            <!-- sensor location map -->
            <v-row class="mb-6">
              <v-col cols="12">
                <v-card elevation="1" rounded="lg">
                  <v-card-title>
                    <h3 class="text-h6 mb-0">Sensor Node Location</h3>
                  </v-card-title>
                  <v-card-text>
                    <LMap
                      v-if="sensorNode?.location"
                      class="rounded-lg"
                      style="height: 400px; width: 100%;"
                      :zoom="13"
                      :center="[sensorNode.location.latitude, sensorNode.location.longitude]"
                    >
                      <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                      <LMarker :lat-lng="[sensorNode.location.latitude, sensorNode.location.longitude]">
                        <LPopup>
                          <div style="min-width: 200px;">
                            <strong>{{ sensorNode.name }}</strong><br />
                            Project: {{ sensorNode.project_uuid }}<br />
                            Last Update: {{ new Date(sensorNode.last_timeseries?.timestamp).toLocaleDateString(userLocale) }}
                          </div>
                        </LPopup>
                      </LMarker>
                    </LMap>
                  </v-card-text>
                  <v-list elevation="1" rounded="lg" density="comfortable" class="mt-4">
                    <v-list-item v-if="sensorNode.location?.altitude">
                      <template #prepend>
                        <v-icon style="font-size: 32px;">mdi-arrow-expand-vertical</v-icon>
                      </template>
                      <v-list-item-title>{{ sensorNode.location.altitude }}</v-list-item-title>
                      <v-list-item-subtitle>Altitude</v-list-item-subtitle>
                    </v-list-item>
                    <v-divider />
                    <v-list-item v-if="sensorNode.location?.postalcode">
                      <template #prepend>
                        <v-icon style="font-size: 32px;">mdi-map-marker</v-icon>
                      </template>
                      <v-list-item-title>{{ sensorNode.location.postalcode }}</v-list-item-title>
                      <v-list-item-subtitle>Postal Code</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                
                </v-card>
              </v-col>
            </v-row>
            <!-- configurables section -->
            <v-row class="mt-6">
            <v-col cols="6">
              <h3 class="text-h6 mb-2">Configurables</h3>
              <v-list elevation="1" rounded="lg" density="comfortable">
                <v-list-item
                  v-for="(config, index) of sensorNode.configurables"
                  :key="index"
                  style="min-height: 72px;"
                  :style="config.type === 'SystemDefined' ? 'background-color: rgba(0,0,0,0.05); font-style: italic;' : ''"
                >
                  <template #prepend>
                    <v-icon style="font-size: 28px;">mdi-cog</v-icon>
                  </template>
                  <v-list-item-title>{{ config.name }}: <strong>{{ config.value }}</strong></v-list-item-title>
                </v-list-item>
              </v-list>
            </v-col>
            <!--  config header file preview -->
            <v-col cols="6">
              <h3 class="text-h6 mb-2">config.h Preview</h3>
              <v-sheet
              elevation="1"
              class="pa-4 position-relative"
              style="background-color: #272822; color: #f8f8f2; font-family: monospace; white-space: pre; overflow: auto; border-radius: 8px; max-height: 300px;"
            >
              {{ configPreview }}
            </v-sheet>
            </v-col>
          </v-row>
          </v-card-text>
        </v-card>
        <v-divider class="my-6" />
        <!-- sensor data -->
        <v-container v-if="sensorNode?.last_timeseries">
          <h2 class="text-h6 mb-2"> Latest Sensor Data</h2>
        <v-list-item-subtitle class="mt-n2 mb-4">
          {{ new Date(sensorNode.last_timeseries.timestamp).toLocaleString(userLocale) }}
        </v-list-item-subtitle>
            <v-data-table
              :items="sensorNode.last_timeseries.fields"
              :headers="fieldHeaders"
              density="compact"
              class="elevation-1 rounded-lg"
              hide-default-footer
              rounded="lg"
              elevation="1"
              disable-sort
            >
              <template #item.value="{ item }">
                {{ item.value }} {{ item.unit }}
              </template>
            </v-data-table>
            </v-container>
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
import { computed } from 'vue'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

const authStore = useAuthStore()
const textStore = useTextStore()
const router = useRouter()
const sensorNode = ref(null)
const loading = ref(true)
const confirmDelete = ref(false)
const sensorNodeToDelete = ref(null)
const deleteConfirmInput = ref('')
const sensorNodeId = ref(useRoute().params.id)
const userLocale = typeof navigator !== 'undefined' ? navigator.language : 'en-US'
const configPreview = computed(() => {
  return sensorNode.value?.configurables?.map(c => `#define ${c.name} ${c.value}`).join('\n') || ''
})
const fieldHeaders = [
  { title: 'Field Name', key: 'field_name' },
  { title: 'Data Type', key: 'protobuf_datatype' },
  { title: 'Value', key: 'value' },
]

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
    // sort configurables by type
    sensorNode.value.configurables.sort((a, b) => a.type.localeCompare(b.type))
  })
  .catch((error) => {
    console.error(`Error fetching sensor node ${sensorNodeId.value}:`, error)
  })
  .finally(() => loading.value = false)

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

const openTTNUrl = () => {
    window.open(sensorNode.value.ttn_device_link, '_blank')
}

// Fix default icon paths for leaflet map (because Vite doesn't automatically handle them)
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).href,
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).href,
})
</script>