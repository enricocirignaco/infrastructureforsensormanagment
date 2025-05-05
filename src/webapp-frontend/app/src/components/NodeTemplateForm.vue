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
            <v-text-field v-model="nodeTemplate.short_name" label="Short Name" :rules="[required]" />
          </v-col>
          <v-col cols="12">
            <v-textarea v-model="nodeTemplate.description" label="Node Template Description" :rules="[required]" />
          </v-col>
          <!-- status dropdown -->
          <v-col v-if="isEditMode" cols="12" sm="6">
            <v-select
              v-model="nodeTemplate.state"
              :items="Object.values(textStore.statusEnum)"
              label="Status"
              :rules="[required]"
            />
          </v-col>
          <v-col cols="12">
            <h3 class="text-h6 mb-2">External Resources</h3>
            <v-row
              v-for="(link, index) in nodeTemplate.external_props"
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
                  :items="Object.values(textStore.externalResourceNodeTemplateEnum)"
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


const addLink = () => {
  nodeTemplate.value.external_props.push({ name: '', url: '', type: '' })
}

const removeLink = (index) => {
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