<template>
  <v-card class="pa-4" v-if="nodeTemplate">
    <v-card-title>{{ isEditMode ? 'Edit Node Template' : 'Create New Node Template' }}</v-card-title>

    <v-form ref="nodeTemplateForm" @submit.prevent="submitNodeTemplate">
      <v-container>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field v-model="nodeTemplate.name" label="Node Template Name" :rules="[required]" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="nodeTemplate.hardware_type" label="Hardware Type" :rules="[required]" />
          </v-col>
          <v-col cols="12">
            <v-textarea v-model="nodeTemplate.description" label="Node Template Description" :rules="[required]" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="nodeTemplate.gitlab_url" label="Gitlab Repository URL" :rules="[required]" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="nodeTemplate.git_ref" label="Git Reference" :rules="[required]" />
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
              <v-col cols="2">
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
              <!-- status dropdown -->
              <v-col cols="2">
                <v-select
                  :items="Object.values(textStore.nodeTemplateStatusEnum)"
                  v-model="field.status"
                  label="Status"
                  :rules="[required]"
                />
              </v-col>
              <!-- commercial senosor dropdown -->
              <v-col cols="2">
                <v-select
                  :items="Object.values(textStore.nodeTemplateStatusEnum)"
                  v-model="field.status"
                  label="Commercial Sensor"
                  :rules="[required]"
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
  <v-container v-else class="d-flex justify-center align-center" style="min-height: 300px">
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

const isEditMode = computed(() => nodeTemplateId !== null)
const nodeTemplateForm = ref(null)
const required = v => !!v || 'Required'
const textStore = useTextStore()
const router = useRouter()
const nodeTemplate = ref(null)

// Define the nodeTemplate object from the nodeTemplate Id or from default values
if(isEditMode.value) {
    // Fetch nodeTemplate data
    nodeTemplateService.getNodeTemplate(nodeTemplateId)
        .then((data) => nodeTemplate.value = data)
        .catch((error) => {
        // TODO: Handle error
        console.error(`Error fetching nodeTemplate ${nodeTemplateId}:`, error)
    })
} else {
  nodeTemplate.value = {
    name: '',
    short_name: '',
    description: '',
    state: '',
    external_props: []
  }
}


const addField = () => {
  nodeTemplate.value.external_props.push({ name: '', url: '', type: '' })
}

const removeField = (index) => {
  nodeTemplate.value.external_props.splice(index, 1)

}

const submitNodeTemplate = () => {
  // Validate Form
  nodeTemplateForm.value?.validate().then((isValid) => {
    if (!isValid.valid) return
    if(isEditMode.value){
        //put request to update the nodeTemplate
        nodeTemplateService.editNodeTemplate(nodeTemplate.value)
            .then((nodeTemplateDTO) => router.push('/nodeTemplate/' + nodeTemplateDTO.uuid))
            .catch((error) => console.log('Error updating nodeTemplate:', error))
    } else {
        // post request to create the nodeTemplate
        nodeTemplateService.createNodeTemplate(nodeTemplate.value)
            .then((nodeTemplateDTO) => router.push('/nodeTemplate/' + nodeTemplateDTO.uuid))
            .catch((error) => console.log('Error creating nodeTemplate:', error))
    }
  })
}
</script>