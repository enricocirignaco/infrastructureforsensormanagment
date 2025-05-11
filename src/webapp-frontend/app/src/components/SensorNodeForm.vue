<template>
  <v-card v-if="isEditMode && sensorNode?.state?.name && sensorNode.state.name !== 'Unused'" class="pa-4">
    <v-card-title>Edit Archived State</v-card-title>
    <v-form ref="sensorNodeForm" @submit.prevent="submitSensorNode">
      <!-- archived checkbox -->
      <v-col v-if="isEditMode"cols="6" class="d-flex align-center">
        <v-checkbox
          v-model="isNodeArchived"
          label="Archive Sensor Node"
          :true-value="true"
          :false-value="false"
          hide-details
        />
      </v-col>
      <v-row>
        <v-col cols="12">
          <v-btn type="submit" color="primary" class="mt-4" block>
            <v-icon start>mdi-content-save</v-icon>
            Save Sensor Node
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-card>

  <!-- main form -->
  <v-card class="pa-4" v-if="(sensorNode && sensorNode.state.name === 'Prepared') || !isEditMode">
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
            />
          </v-col>
          <v-col cols="12">
            <v-textarea v-model="sensorNode.description" label="Sensor Node Description" :rules="[required]" />
          </v-col>
          
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
                      :zoom="6"
                      :center="[46.8, 8.2]"
                      @click="e => {
                        sensorNode.location.latitude = e.latlng.lat
                        sensorNode.location.langitude = e.latlng.lng
                      }"
                    >
                      <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                      <LMarker
                        v-if="sensorNode.location.latitude && sensorNode.location.langitude"
                        :lat-lng="[sensorNode.location.latitude, sensorNode.location.langitude]"
                      />
                    </LMap>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col v-if="!showMap" cols="12" sm="6">
                    <v-text-field v-model="sensorNode.location.latitude" type='number' label="Latitude" :rules="[locationConditionalRule()]" />
                  </v-col>
                  <v-col v-if="!showMap" cols="12" sm="6">
                    <v-text-field v-model="sensorNode.location.langitude" type='number' label="Longitude" :rules="[locationConditionalRule()]" />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field v-model="sensorNode.location.altitude" type='number' label="Altitude" :rules="[locationConditionalRule()]" />
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field v-model="sensorNode.location.postalcode" type='number' label="Postal code" :rules="[locationConditionalRule()]" />
                  </v-col>
                </v-row>
                
              </v-card-text>
            </v-card>
          </v-col>
          
          <!-- Configurables -->
          <v-col cols="12">
            <h3 class="text-h6 mb-2">Configurables</h3>
            <v-row
              v-for="(config, index) in sensorNode.configurables.filter(c => c.type === 'UserDefined')"
              :key="index"
              class="mb-2"
            >
              <v-col cols="6">
                <v-text-field
                  v-model="config.name"
                  label="Name"
                  :rules="[required]"
                />
              </v-col>
              <v-col cols="5">
                <v-text-field
                :model-value="config.value"
                label="Value"
                :rules="[required]"
                />
              </v-col> 
            </v-row>
          </v-col>
          <!-- Fields -->
          <v-col cols="12">
            <h3 class="text-h6 mb-2">Sensor Node Fields</h3>
            <v-row
              v-for="(field, index) in sensorNode.fields"
              :key="index"
              class="mb-2"
            >
              <v-col cols="3">
                <v-text-field v-model="field.field_name" label="Name" :rules="[required]" />
              </v-col>
              <!-- protobuf type dropdown -->
              <v-col cols="3">
                <v-select
                  :items="Object.values(textStore.ProtobufDataTypes)"
                  v-model="field.protbuf_datatype"
                  label="ProtoBuf Data Type"
                  :rules="[required]"
                />
              </v-col>
              <!-- unit dropdown -->
              <v-col cols="2">
                <v-select
                  :items="Object.values(textStore.sensorUnitsEnum)"
                  v-model="field.unit"
                  label="Unit"
                  :rules="[required]"
                />
              </v-col>
              
              <!-- commercial senosor dropdown -->
              <v-col cols="3">
                <v-select
                  :items="Object.values(commercialSensorsDTO)"
                  v-model="field.commercial_sensor"
                  label="Commercial Sensor"
                  item-title="alias"
                  item-value="uuid"
                  return-object
                />
              </v-col>
              <!-- delete button -->
              <v-col cols="1" class="d-flex align-center">
                <v-btn icon @click="removeField(index)" color="secondary">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-btn @click="addField" rounded="lg" color="primary">
              <v-icon start>mdi-plus</v-icon>
              Add Field
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-btn type="submit" color="primary" class="mt-4" block>
              <v-icon start>mdi-content-save</v-icon>
              Save Sensor Node
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
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

const showMap = ref(false)
const isEditMode = computed(() => sensorNodeId !== null)
const sensorNodeForm = ref(null)
const required = v => !!v || 'Required'
const textStore = useTextStore()
const router = useRouter()
const sensorNode = ref(null)
const isNodeArchived = ref(false)
const nodeTemplates = ref([])
// Define the sensorNode object from the sensorNode Id or from default values
if (isEditMode.value) {
  // Fetch sensorNode data
  sensorNodeService.getSensorNode(sensorNodeId)
    .then((data) => {
      sensorNode.value = data

      // Map state
      const matchedState = Object.values(textStore.sensorNodeStatusEnum).find(
        s => s.name === data.state
      )
      sensorNode.value.state = {
        name: data.state,
        label: matchedState ? matchedState.label : data.state,
        color: matchedState ? matchedState.color : 'grey'
      }
      // set the archived state
      sensorNode.value.state.name === 'Archived' ? isNodeArchived.value = true : isNodeArchived.value = false
    })
    .catch((error) => {
      console.error(`Error fetching node sensor node ${sensorNodeId}:`, error)
    })
} else {
  sensorNode.value = {
    name: '',
    description: '',
    location: {
      latitude: '',
      langitude: '',
      altitude: '',
      postalcode: '',
    },
    configurables: [],
    state: {
      name: '',
      label: '',
      color: ''
    },
    fields: [],
  }
}
// fetch node templates
nodeTemplateService.getNodeTemplatesDTO()
  .then((data) => {
    nodeTemplates.value = data
  })
  .catch((error) => {
    console.error('Error fetching node templates:', error)
  })

// Custom rule: location fields required if any location field is filled
const locationConditionalRule = () => {
  const loc = sensorNode.value.location
  const isAnyFilled = loc.latitude || loc.langitude || loc.altitude || loc.postalcode
  return v => !isAnyFilled || !!v || 'Required if any location field is filled'
}

const addField = () => {
  sensorNode.value.fields.push({ name: '', protbuf_datatype: '', unit: '', commercial_sensor: null })
}

const removeField = (index) => {
  sensorNode.value.fields.splice(index, 1)

}
const addConfigurable = () => {
  sensorNode.value.configurables.push({ name: '', type: 'UserDefined'})
}
const removeConfigurable = (index) => {
  sensorNode.value.configurables.splice(index, 1)
}

const submitSensorNode = () => {
  // Validate Form
  sensorNodeForm.value?.validate().then((isValid) => {
    if (!isValid.valid) return
    computeState()
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

const computeState = () => {
  if(isNodeArchived.value){
    sensorNode.value.state = 'Archived'
  } else {
    sensorNode.value.inherited_sensor_nodes != null && sensorNode.value.inherited_sensor_nodes.length === 0 ? sensorNode.value.state = 'Unused' : sensorNode.value.state = 'In-use'
  }
}
</script>