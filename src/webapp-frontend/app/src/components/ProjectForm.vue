<template>
  <!-- Archived View -->
   <v-card v-if="isEditMode && project?.state && project.state !== 'Prepared'" class="pa-4">
    <v-card-title>Edit Archived State</v-card-title>
    <v-form ref="projectForm" @submit.prevent="submitProject">
      <!-- archived checkbox -->
      <v-col v-if="project.state !== 'Prepared'" cols="6" class="d-flex align-center">
        <v-checkbox
          v-model="project.state"
          label="Archive Project"
          :true-value="'Archived'"
          :false-value="'Active'"
          hide-details
        />
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
            Save Project
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



  <v-card class="pa-4" v-if="(project && project?.state === 'Prepared') || !isEditMode">
    <v-card-title>{{ isEditMode ? 'Edit Project' : 'Create New Project' }}</v-card-title>

    <v-form ref="projectForm" @submit.prevent="submitProject">
      <v-container>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field v-model="project.name" label="Project Name" :rules="[required]" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="project.short_name" label="Short Name" :rules="[required]" />
          </v-col>
          <v-col cols="12">
            <v-textarea v-model="project.description" label="Project Description" :rules="[required]" />
          </v-col>
          <v-col cols="12">
            <h3 class="text-h6 mb-2">External Resources</h3>
            <v-row
              v-for="(link, index) in project.external_props"
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
                  :items="Object.values(textStore.externalResourceProjectEnum)"
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
          <v-col cols="6">
            <v-btn
            type="submit"
            color="primary"
            class="mt-4"
            block
            :disabled="isSubmitting"
            >
              <v-icon start>mdi-content-save</v-icon>
              Save Project
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
  <!-- loading animation -->
  <v-container v-if="!isEditMode && !project" class="d-flex justify-center align-center" style="min-height: 300px">
    <v-progress-circular indeterminate color="primary" size="64" />
  </v-container>
</template>

<script setup>
// defineProps of the component
const { projectId } = defineProps({
  projectId: {
    type: String,
    default: null
  }
})

import { ref } from 'vue'
import { computed } from 'vue'
import { useTextStore} from '@/stores/textStore'
import { useRouter } from 'vue-router'
import projectService from '@/services/projectService'

const isEditMode = computed(() => projectId !== null)
const projectForm = ref(null)
const required = v => !!v || 'Required'
const textStore = useTextStore()
const router = useRouter()
const project = ref(null)
const isSubmitting = ref(false)
// Define the project object from the project Id or from default values
if(isEditMode.value) {
    // Fetch project data
    projectService.getProject(projectId)
        .then((data) => {
          project.value = data
          console.log('Fetched project:', project.value)
        })
        .catch((error) => {
        // TODO: Handle error
        console.error(`Error fetching project ${projectId}:`, error)
    })
} else {
  project.value = {
    name: '',
    short_name: '',
    description: '',
    state: '',
    external_props: []
  }
}


const addLink = () => {
  project.value.external_props.push({ name: '', url: '', type: '' })
}

const removeLink = (index) => {
  project.value.external_props.splice(index, 1)

}

const submitProject = () => {
  isSubmitting.value = true
  // Validate Form
  projectForm.value?.validate().then((isValid) => {
    if (!isValid.valid) return
    if(isEditMode.value){
        //put request to update the project
        projectService.editProject(project.value)
            .then((projectDTO) => router.push('/project/' + projectDTO.uuid))
            .catch((error) => console.log('Error updating project:', error))
    } else {
        // post request to create the project
        projectService.createProject(project.value)
            .then((projectDTO) => router.push('/project/' + projectDTO.uuid))
            .catch((error) => console.log('Error creating project:', error))
    }
  })
}
</script>