<template>

  <v-card v-if="isEditMode && sensorNode?.state && sensorNode.state !== 'Prepared'" class="pa-4">
    <v-card-title>Edit Archived State</v-card-title>
    <v-form ref="sensorNodeForm" @submit.prevent="submitSensorNode">
      <!-- archived checkbox -->
      <v-col v-if="sensorNode.state !== 'Active'" cols="6" class="d-flex align-center">
        <v-checkbox
          v-model="sensorNode.state"
          label="Archive Sensor Node"
          :true-value="'Archived'"
          :false-value="'Inactive'"
          hide-details
        />
      </v-col>
      <v-col cols="12">
        <v-textarea v-if="sensorNode.state !== 'Archived' "v-model="sensorNode.description" label="Notes" />
      </v-col>
      <v-row>
        <v-col cols="6">
          <v-btn
          type="submit"
          color="primary"
          class="mt-4"
          block
          :disabled="isSubmitting"
          >
            <v-icon start>mdi-content-save</v-icon>
            Save Sensor Node
          </v-btn>
        </v-col>
        <v-col cols="6">
            <v-btn color="secondary" class="mt-4" block @click="router.back()">
              <v-icon start>mdi-close</v-icon>
              Cancel
            </v-btn>
          </v-col>
      </v-row>
    </v-form>
  </v-card>

  <!-- main form -->
  <v-card class="pa-4" v-if="(sensorNode && sensorNode?.state === 'Prepared') || !isEditMode">
    <v-card-title>{{ isEditMode ? 'Edit Sensor Node' : 'Create New Sensor Node' }}</v-card-title>
    <v-form ref="sensorNodeForm" @submit.prevent="submitSensorNode">
      <v-container>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field v-model="sensorNode.name" label="Sensor Node Name" :rules="[required]" />
          </v-col>
          <!-- node template dropdown -->
          <v-col cols="12" sm="6">
            <v-select
              :items="Object.values(nodeTemplates)"
              v-model="sensorNode.node_template_uuid"
              label="Node Template"
              item-title="name"
              item-value="uuid"
              :rules="[required]"
              @update:modelValue="loadConfigurables"
            />
          </v-col>
          <v-col cols="12">
            <v-textarea v-model="sensorNode.description" label="Notes" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="sensorNode.gitlab_ref" label="Gitlab Ref" :rules="[required]" />
          </v-col>
          <!-- location -->
          <v-col cols="12">
            <v-card outlined>
              <v-card-title class="text-subtitle-1 d-flex justify-space-between align-center">
                <span>Location</span>
                <v-btn rounded="lg" color="primary" @click="showMap = !showMap">
                  <v-icon start>mdi-map-marker</v-icon>
                  {{ showMap ? 'Hide Map' : 'Show Map' }}
                </v-btn>
              </v-card-title>
              <v-card-text>
                <!-- map -->
                <v-row v-if="showMap">
                  <v-col cols="12">
                    <LMap
                      style="height: 300px"
                      :zoom="12"
                      :center="[sensorNode.location.latitude || textStore.newMapDefaultLocation.lat, sensorNode.location.longitude || textStore.newMapDefaultLocation.lng]"
                      @click="e => {
                        sensorNode.location.latitude = e.latlng.lat
                        sensorNode.location.longitude = e.latlng.lng
                      }"
                    >
                      <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                      <LMarker
                        v-if="sensorNode.location.latitude && sensorNode.location.longitude"
                        :lat-lng="[sensorNode.location.latitude, sensorNode.location.longitude]"
                      />
                    </LMap>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col v-if="!showMap" cols="12" sm="6">
                    <v-text-field v-model="sensorNode.location.latitude" type='number' label="Latitude" />
                  </v-col>
                  <v-col v-if="!showMap" cols="12" sm="6">
                    <v-text-field v-model="sensorNode.location.longitude" type='number' label="Longitude" />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                    v-model.number="sensorNode.location.altitude"
                    type='number'
                    label="Altitude"
                    @blur="sensorNode.location.altitude = sensorNode.location.altitude === '' ? null : sensorNode.location.altitude"
                    />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                    v-model.number="sensorNode.location.postalcode"
                    type='number'
                    label="Postal code"
                    @blur="sensorNode.location.postalcode = sensorNode.location.postalcode === '' ? null : sensorNode.location.postalcode"
                    />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
          
          <!-- Configurables -->
          <v-col v-if="showConfigurables || isEditMode" cols="12">
            <v-card outlined>
              <v-card-title class="text-subtitle-1">Configurables</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="6">
                    <v-row
                      v-for="(config, index) in sensorNode.configurables.filter(c => c.type === 'UserDefined')"
                      :key="index"
                      class="mb-2"
                    >
                      <v-col cols="6" class="d-flex align-center">
                        <span class="text-subtitle-2">{{ config.name }}</span>
                      </v-col>
                      <v-col cols="6">
                        <v-text-field
                          v-model="config.value"
                          label="Value"
                          :rules="[required]"
                        />
                      </v-col>
                    </v-row>
                  </v-col>
                  <v-col cols="6">
                   <v-alert type="info" variant="tonal" border="start" border-color="primary" class="ma-2" style="white-space: pre-wrap;">
                      {{ textStore.configurablesWarning }}
                    </v-alert>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
            <!-- Message Banner -->
          <Banner
              v-if="bannerMessage !== ''"
              type="info"
              :message="bannerMessage"
          ></Banner>
        </v-row>
        <v-row>
          <v-col :cols="isEditMode ? 6 : 4">
            <v-btn
            type="submit"
            color="primary"
            class="mt-4"
            block
            :disabled="isSubmitting"
            >
              <v-icon start>mdi-content-save</v-icon>
              Save
            </v-btn>
          </v-col>
          <v-col v-if="!isEditMode" cols="4">
            <v-btn
            color="primary"
            class="mt-4"
            block
            :disabled="isSubmitting"
            @click="submitAndCreateAnother"
            >
              <v-icon start>mdi-content-save</v-icon>
              Save and Create Another
            </v-btn>
          </v-col>
          <v-col :cols="isEditMode ? 6 : 4">
            <v-btn color="secondary" class="mt-4" block @click="router.back()">
              <v-icon start>mdi-close</v-icon>
              Cancel
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>

  <!-- loading animation -->
  <v-container v-if="!isEditMode && !sensorNode" class="d-flex justify-center align-center" style="min-height: 300px">
    <v-progress-circular indeterminate color="primary" size="64" />
  </v-container>

</template>

<script setup>
// defineProps of the component
const { sensorNodeId } = defineProps({
  sensorNodeId: {
    type: String,
    default: null
  }
})

import { ref } from 'vue'
import { computed } from 'vue'
import { useTextStore} from '@/stores/textStore'
import { useRouter } from 'vue-router'
import sensorNodeService from '@/services/sensorNodeService'
import nodeTemplateService from '@/services/nodeTemplateService'
import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import { useRoute } from 'vue-router'
import Banner from '@/components/Banner.vue'
import { nextTick } from 'vue'
const route = useRoute()
const showMap = ref(false)
const isEditMode = computed(() => sensorNodeId !== null)
const sensorNodeForm = ref(null)
const required = v => !!v || 'Required'
const textStore = useTextStore()
const router = useRouter()
const sensorNode = ref(null)
const nodeTemplates = ref([])
const showConfigurables = ref(false)
const isSubmitting = ref(false)
const bannerMessage = ref('')
// Define the sensorNode object from the sensorNode Id or from default values
if (isEditMode.value) {
  // Fetch sensorNode data
  sensorNodeService.getSensorNode(sensorNodeId)
    .then((data) => {
      sensorNode.value = data
    })
    .catch((error) => {
      console.error(`Error fetching node sensor node ${sensorNodeId}:`, error)
    })
} else {
  sensorNode.value = {
    name: '',
    description: '',
    node_template_uuid: '',
    project_uuid: `${route.query.project_uuid}`,
    location: {
      latitude: null,
      longitude: null,
      altitude: null,
      postalcode: null,
    },
    configurables: [],
    gitlab_ref: '',
  }
}
// fetch node templates
  nodeTemplateService.getNodeTemplatesDTO()
    .then((data) => nodeTemplates.value = data)
    .catch((error) => console.error('Error fetching node templates:', error))

// get configurables from the node template
function loadConfigurables(nodeTemplateUuid) {
  // fetch node template
  nodeTemplateService.getNodeTemplate(nodeTemplateUuid)
    .then((data) => {
      // load configurables from the node template to the sensorNode
      sensorNode.value.configurables = data.configurables
        .filter((config) => config.type === 'UserDefined')
        .map((config) => {
          return {
            name: config.name,
            type: config.type,
            value: config.value
          }
        })
      showConfigurables.value = true
    })
    .catch((error) => {
      console.error('Error fetching node templates:', error)
    })
}

const submitSensorNode = () => {
  // Validate Form
  sensorNodeForm.value?.validate().then((isValid) => {
    if (!isValid.valid) return
    isSubmitting.value = true
    if(isEditMode.value){
        //put request to update the sensorNode
        sensorNodeService.editSensorNode(sensorNode.value)
            .then((sensorNode) => router.push('/sensor-node/' + sensorNode.uuid))
            .catch((error) => console.log('Error updating sensorNode:', error))
    } else {
        // post request to create the sensorNode
        sensorNodeService.createSensorNode(sensorNode.value)
            .then((sensorNode) => router.push('/sensor-node/' + sensorNode.uuid))
            .catch((error) => console.log('Error creating sensorNode:', error))
    }
  })
}

  const submitAndCreateAnother = () => {
  // Validate Form
  sensorNodeForm.value?.validate().then((isValid) => {
    if (!isValid.valid) return
    isSubmitting.value = true

    // post request to create the sensorNode
    sensorNodeService.createSensorNode(sensorNode.value)
        .then((sensorNode) => {
          isSubmitting.value = false
          // reset banner message first to force reactivity
          bannerMessage.value = ''
          nextTick(() => {
            bannerMessage.value = `New Sensor Node created successfully. UUID: ${sensorNode.uuid}     You can now create another one.`
          })
        })
        .catch((error) => console.log('Error creating sensorNode:', error))
  })
}

</script>