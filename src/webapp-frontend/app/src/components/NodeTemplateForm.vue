<template>
  <v-card v-if="isEditMode && nodeTemplate && nodeTemplate.state.name !== 'Unused'" class="pa-4">
    <v-card-title>Edit Archived State</v-card-title>
    <v-form ref="nodeTemplateForm" @submit.prevent="submitNodeTemplate">
      <!-- archived checkbox -->
      <v-col v-if="isEditMode"cols="6" class="d-flex align-center">
        <v-checkbox
          v-model="isNodeArchived"
          label="Archive Node Template"
          :true-value="true"
          :false-value="false"
          hide-details
        />
      </v-col>
      <v-row>
        <v-col cols="12">
          <v-btn type="submit" color="primary" class="mt-4" block>
            <v-icon start>mdi-content-save</v-icon>
            Save Node Template
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-card>
  <v-card class="pa-4" v-if="(nodeTemplate && nodeTemplate.state.name === 'Unused') || !isEditMode">
    <v-card-title>{{ isEditMode ? 'Edit Node Template' : 'Create New Node Template' }}</v-card-title>

    <v-form ref="nodeTemplateForm" @submit.prevent="submitNodeTemplate">
      <v-container>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field v-model="nodeTemplate.name" label="Node Template Name" :rules="[required]" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="nodeTemplate.gitlab_url" label="Gitlab Repository URL" :rules="[required]" />
          </v-col>
          <v-col cols="12">
            <v-textarea v-model="nodeTemplate.description" label="Node Template Description" :rules="[required]" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="nodeTemplate.board.core" label="Hardware Core" :rules="[required]" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="nodeTemplate.board.variant" label="Hardware Variant" :rules="[required]" />
          </v-col>
          
          <!-- Configurables -->
          <v-col cols="12">
            <h3 class="text-h6 mb-2">Configurables</h3>
            <v-row
              v-for="(config, index) in nodeTemplate.configurables.filter(c => c.type === 'UserDefined')"
              :key="index"
              class="mb-2"
            >
              <v-col cols="5">
                <v-text-field
                :model-value="config.name"
                @update:model-value="val => config.name = val.toUpperCase()"
                label="Name"
                :rules="[required]"
                />
              </v-col>

              <!-- delete button -->
              <v-col cols="1" class="d-flex align-center">
                <v-btn icon @click="removeConfigurable(index)" color="secondary">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-btn @click="addConfigurable" rounded="lg" color="primary">
              <v-icon start>mdi-plus</v-icon>
              Add Config
            </v-btn>
          </v-col>
          <!-- Fields -->
          <v-col cols="12">
            <h3 class="text-h6 mb-2">Node Template Fields</h3>
            <v-row
              v-for="(field, index) in nodeTemplate.fields"
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
              Save Node Template
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
  <v-container v-if="!isEditMode && !nodeTemplate" class="d-flex justify-center align-center" style="min-height: 300px">
    <v-progress-circular indeterminate color="primary" size="64" />
  </v-container>
</template>

<script setup>
// defineProps of the component
const { nodeTemplateId } = defineProps({
  nodeTemplateId: {
    type: String,
    default: null
  }
})

import { ref } from 'vue'
import { computed } from 'vue'
import { useTextStore} from '@/stores/textStore'
import { useRouter } from 'vue-router'
import nodeTemplateService from '@/services/nodeTemplateService'
import commercialSensorService from '@/services/commercialSensorService'

const isEditMode = computed(() => nodeTemplateId !== null)
const nodeTemplateForm = ref(null)
const required = v => !!v || 'Required'
const textStore = useTextStore()
const router = useRouter()
const nodeTemplate = ref(null)
const commercialSensorsDTO = ref([])
const isNodeArchived = ref(false)

// Define the nodeTemplate object from the nodeTemplate Id or from default values
if (isEditMode.value) {
  // Fetch nodeTemplate data
  nodeTemplateService.getNodeTemplate(nodeTemplateId)
    .then((data) => {
      nodeTemplate.value = data

      // Map state
      const matchedState = Object.values(textStore.nodeTemplateStatusEnum).find(
        s => s.name === data.state
      )
      nodeTemplate.value.state = {
        name: data.state,
        label: matchedState ? matchedState.label : data.state,
        color: matchedState ? matchedState.color : 'grey'
      }
      // set the archived state
      nodeTemplate.value.state.name === 'Archived' ? isNodeArchived.value = true : isNodeArchived.value = false
    })
    .catch((error) => {
      console.error(`Error fetching node template ${nodeTemplateId}:`, error)
    })
} else {
  nodeTemplate.value = {
    name: '',
    description: '',
    gitlab_url: '',
    board: {
      core: '',
      variant: ''
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

// Fetch commercial sensors data
commercialSensorService.getCommercialSensorsDTO()
  .then((data) => commercialSensorsDTO.value = data)
  .catch((error) => {
    console.error(`Error fetching commercial sensors:`, error)
  })

const addField = () => {
  nodeTemplate.value.fields.push({ name: '', protbuf_datatype: '', unit: '', commercial_sensor: null })
}

const removeField = (index) => {
  nodeTemplate.value.fields.splice(index, 1)

}
const addConfigurable = () => {
  nodeTemplate.value.configurables.push({ name: '', type: 'UserDefined'})
}
const removeConfigurable = (index) => {
  nodeTemplate.value.configurables.splice(index, 1)
}

const submitNodeTemplate = () => {
  // Validate Form
  nodeTemplateForm.value?.validate().then((isValid) => {
    if (!isValid.valid) return
    console.log('nodeTemplate.value', nodeTemplate.value)

    computeState()
    if(isEditMode.value){
        //put request to update the nodeTemplate
        nodeTemplateService.editNodeTemplate(nodeTemplate.value)
            .then((nodeTemplate) => router.push('/node-template/' + nodeTemplate.uuid))
            .catch((error) => console.log('Error updating nodeTemplate:', error))
    } else {
        // post request to create the nodeTemplate
        nodeTemplateService.createNodeTemplate(nodeTemplate.value)
            .then((nodeTemplate) => router.push('/node-template/' + nodeTemplate.uuid))
            .catch((error) => console.log('Error creating nodeTemplate:', error))
    }
  })
}

const computeState = () => {
  if(isNodeArchived.value){
    nodeTemplate.value.state = 'Archived'
  } else {
    nodeTemplate.value.inherited_sensor_nodes != null && nodeTemplate.value.inherited_sensor_nodes.length === 0 ? nodeTemplate.value.state = 'Unused' : nodeTemplate.value.state = 'In-use'
  }
}
</script>