<template>
  <v-card class="pa-4" v-if="project">
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
          <!-- status dropdown -->
          <v-col v-if="isEditMode" cols="12" sm="6">
            <v-select
              v-model="project.state"
              :items="Object.values(textStore.statusEnum)"
              label="Status"
              :rules="[required]"
            />
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
                  :items="Object.values(textStore.externalResourceTypeEnum)"
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
              Save Project
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

// Define the project object from the project Id or from default values
if(isEditMode.value) {
    // Fetch project data
    projectService.getProject(projectId)
        .then((data) => project.value = data)
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