<template>
  <v-card class="pa-4" v-if="sensor">
    <v-card-title>{{ isEditMode ? 'Edit Sensor' : 'Create New Sensor' }}</v-card-title>

    <v-form ref="sensorForm" @submit.prevent="submitSensor">
      <v-container>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field v-model="sensor.name" label="Sensor Name" :rules="[required]" required />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="sensor.alias" label="Sensor Alias" :rules="[required]" required />
          </v-col>
          <v-col cols="12">
            <v-textarea v-model="sensor.description" label="Sensor Description" :rules="[required]" required />
          </v-col>
          <!-- External properties section -->
          <v-col cols="12">
            <h3 class="text-h6 mb-2">External Resources</h3>
            <v-row
              v-for="(link, index) in sensor.external_props"
              :key="index"
              class="mb-2"
            >
              <v-col cols="4">
                <v-text-field v-model="link.name" label="Name" :rules="[required]" />
              </v-col>
              <v-col cols="4">
                <v-text-field v-model="link.url" label="URL" :rules="[required]" />
              </v-col>
              <v-col cols="3">
                <!-- external resource type dropdown -->
                <v-select
                  v-model="link.type"
                  :items="Object.values(textStore.externalResourceSensorEnum)"
                  label="Type"
                  :rules="[required]"
                />
              </v-col>
              <v-col cols="1" class="d-flex align-center">
                <v-btn icon @click="removeLink(index)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-btn @click="addLink" rounded="lg" color="primary">
              <v-icon start>mdi-plus</v-icon>
              Add Resource
            </v-btn>
          </v-col>
          <!-- Sensor Properties Section -->
          <v-col cols="12">
            <h3 class="text-h6 mb-2">Sensor Properties</h3>
            <v-row
              v-for="(prop, index) in sensor.sensor_props"
              :key="index"
              class="mb-2"
            >
              <v-col cols="4">
                <v-text-field
                  v-model="prop.name"
                  label="Name"
                  :rules="[required]"
                />
              </v-col>
              <v-col cols="2">
                <v-select
                  v-model="prop.unit"
                  :items="Object.values(textStore.sensorUnitsEnum)"
                  label="Unit"
                  :rules="[required]"
                />
              </v-col>
              <v-col cols="2">
                <v-text-field
                  v-model="prop.precision"
                  label="Precision"
                  :suffix="prop.unit"
                  prefix="±"
                  type="number"
                  :rules="[required]"
                />
              </v-col>
              <v-col cols="3">
                <v-row dense>
                  <v-col cols="5">
                    <v-text-field
                    v-model="prop.range.min"
                    label="Min"
                    :suffix="prop.unit"
                    type="number"
                    :rules="[required]"
                    />
                  </v-col>
                  <v-col cols="2" class="d-flex align-center justify-center text-medium-emphasis">
                    to
                  </v-col>
                  <v-col cols="5">
                    <v-text-field
                    v-model="prop.range.max"
                    label="Max"
                    :suffix="prop.unit"
                    type="number"
                    :rules="[required]"
                    />
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="auto" class="d-flex align-center">
                <v-btn icon @click="removeSensorProp(index)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-btn @click="addSensorProp" rounded="lg" color="primary">
              <v-icon start>mdi-plus</v-icon>
              Add Property
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6">
            <v-btn type="submit" color="primary" class="mt-4" block>
              <v-icon start>mdi-content-save</v-icon>
              Save
            </v-btn>
          </v-col>
          <v-col cols="6">
            <v-btn color="secondary" class="mt-4" block @click="router.back()">
              <v-icon start>mdi-close</v-icon>
              Cancel
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
  <v-container v-else class="d-flex justify-center align-center" style="min-height: 300px">
    <v-progress-circular indeterminate color="primary" size="64" />
  </v-container>
</template>

<script setup>
// defineProps of the component
const { sensorId } = defineProps({
  sensorId: {
    type: String,
    default: null
  }
})

import { ref } from 'vue'
import { computed } from 'vue'
import { useTextStore} from '@/stores/textStore'
import { useRouter } from 'vue-router'
import commercialSensorService from '@/services/commercialSensorService'

const isEditMode = computed(() => sensorId !== null)
const sensorForm = ref(null)
const required = v => !!v || 'Required'
const textStore = useTextStore()
const router = useRouter()
const sensor = ref(null)

// Define the sensor object from the sensor Id or from default values
if(isEditMode.value) {
    // Fetch sensor data
    commercialSensorService.getCommercialSensor(sensorId)
        .then((data) => sensor.value = data)
        .catch((error) => {
          // TODO: Handle error
          console.error(`Error fetching sensor ${sensorId}:`, error)
        })
} else {
  sensor.value = {
    name: '',
    alias: '',
    description: '',
    external_props: [],
    sensor_props: [],
  }
}


const addLink = () => {
  sensor.value.external_props.push({ name: '', url: '', type: '' })
}

const removeLink = (index) => {
  sensor.value.external_props.splice(index, 1)

}

const addSensorProp = () => {
  sensor.value.sensor_props.push({
    name: '',
    value: '',
    unit: '',
    precision: '',
    range:
      {
        min: '',
        max: ''
      }
  })
}

const removeSensorProp = (index) => {
  sensor.value.sensor_props.splice(index, 1)
}
const submitSensor = () => {
  // Validate Form
  sensorForm.value?.validate().then((isValid) => {
    if (!isValid.valid) return
    if (isEditMode.value) {
      commercialSensorService.editCommercialSensor(sensor.value)
        .then((sensorDTO) => router.push('/commercial-sensor/' + sensorDTO.uuid))
        .catch((error) => console.log('Error updating sensor:', error))
    } else {
      commercialSensorService.createCommercialSensor(sensor.value)
        .then((sensorDTO) => router.push('/commercial-sensor/' + sensorDTO.uuid))
        .catch((error) => console.log('Error creating sensor:', error))
    }
  })
}
</script>