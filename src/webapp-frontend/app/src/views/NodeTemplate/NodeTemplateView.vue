<template>
  <!-- Loading Animation -->
  <v-container v-if="loading" class="d-flex justify-center align-center" style="min-height: 300px">
    <v-progress-circular indeterminate color="primary" size="64" />
  </v-container>
  <v-container v-else>
    <v-row>
      <v-col cols="9">
        <!-- Node Template Details -->
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
                    <h2 class="mb-0">{{ nodeTemplate.name }}</h2>
                </v-col>
                <v-col cols="auto" class="d-flex align-center">
                  <!-- state-->
                  <v-chip
                  :color="nodeTemplate.state.color"
                  variant="flat"
                  class="me-2 text-white"
                  >
                    {{ nodeTemplate.state.label }}
                  </v-chip>
                  <!-- edit button -->
                  <v-btn
                  v-if="authStore.getUser?.role !== 'Researcher'"
                  color="primary"
                  icon size="small"
                  class="me-1"
                  @click="router.push(`/node-template/${nodeTemplateId}/edit`)"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <!-- delete button -->
                  <v-btn
                  v-if="authStore.getUser?.role !== 'Researcher' && nodeTemplate.state.name === 'Unused'"
                  color="error"
                  icon size="small"
                  @click="deletenodeTemplate(nodeTemplateId)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-col>
            </v-row>
          </v-card-title>
          <v-divider class="my-6" />
          <!-- Node Template content -->
          <v-card-text>
            <div class="mb-6">
              <h3 class="text-h6 mb-2">Description</h3>
              <p class="text-body-1">{{ nodeTemplate.description }}</p>
            </div>
            <v-list elevation="1" rounded="lg" density="comfortable">
              <v-list-item
                style="min-height: 72px; cursor: pointer;"
                @click="openGitlabUrl"
              >
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-source-repository</v-icon>
                </template>
                <v-list-item-title>{{ nodeTemplate.gitlab_url }}</v-list-item-title>
                <v-list-item-subtitle>GitLab URL</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-chip</v-icon>
                </template>
                <v-list-item-title>{{nodeTemplate.board.core}}</v-list-item-title>
                <v-list-item-subtitle>Hardware Core</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-chip</v-icon>
                </template>
                <v-list-item-title>{{ nodeTemplate.board.variant }}</v-list-item-title>
                <v-list-item-subtitle>Hardware Variant</v-list-item-subtitle>
              </v-list-item>
              <v-divider />
              <v-list-item style="min-height: 72px;">
                <template #prepend>
                  <v-icon style="font-size: 32px;">mdi-identifier</v-icon>
                </template>
                <v-list-item-title>{{ nodeTemplate.uuid }}</v-list-item-title>
                <v-list-item-subtitle>UUID</v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <!-- configurables section -->
            <v-row class="mt-6">
            <v-col cols="6">
              <h3 class="text-h6 mb-2">Configurables</h3>
              <v-list elevation="1" rounded="lg" density="comfortable">
                <v-list-item
                  v-for="(config, index) in nodeTemplate.configurables"
                  :key="index"
                  style="min-height: 72px;"
                  :style="config.type === 'SystemDefined' ? 'background-color: rgba(0,0,0,0.05); font-style: italic;' : ''"


                >
                  <template #prepend>
                    <v-icon style="font-size: 28px;">mdi-cog</v-icon>
                  </template>
                  <v-list-item-title>{{ config.name }}</v-list-item-title>
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


            <!-- Fields Table -->
            <h3 class="text-h6 mb-2 mt-6">Fields</h3>
            <v-data-table
              :items="nodeTemplate.fields"
              :headers="fieldHeaders"
              density="compact"
              class="elevation-1 rounded-lg"
              hide-default-footer
              rounded="lg"
              elevation="1"
              disable-sort
            >
            <template  #item.commercial_sensor="{ item }">
              <v-btn v-if="item.commercial_sensor?.uuid"
                variant="outlined"
                color="secondary"
                size="small"
                rounded
                :to="`/commercial-sensor/${item.commercial_sensor?.uuid}`"
                style="text-transform: none; min-width: 150px;"
                
              >
                <v-icon start class="me-1">mdi-link-variant</v-icon>
                {{ item.commercial_sensor?.alias }}
              </v-btn>
            </template>
            </v-data-table>

            <!-- protobuff scheme -->
            <v-row class="align-center mb-2 mt-6">
              <v-col>
                <h3 class="text-h6 mb-0">Protobuf Scheme</h3>
              </v-col>
              <v-col cols="auto">
                <v-btn
                  color="secondary"
                  size="small"
                  :href="`/node-template/${nodeTemplateId}/code`"
                  download
                  style="text-transform: none;"
                >
                  <v-icon start class="me-1">mdi-download</v-icon>
                  Download NanoPB Code
                </v-btn>
              </v-col>
            </v-row>
            <v-sheet
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
              {{ protobuf_schema.schema }}
            </v-sheet>
          </v-card-text>
        </v-card>
        <v-divider class="my-6" />
        

        <h2 class="text-h6 mb-2">Deployed Nodes</h2>
        <!-- Table of deployed nodes -->
        <v-data-table
          :items="nodeTemplate.inherited_sensor_nodes"
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
        </v-data-table>
      </v-col>
      <!-- Logbook -->
      <v-col cols="3">
        <Logbook v-if="nodeTemplate?.logbook" :logbook="nodeTemplate.logbook" />
      </v-col>
    </v-row>
  </v-container>


  
  <!-- delete dialog -->
  <v-dialog v-model="confirmDelete" max-width="500">
    <v-card>
      <v-card-title class="text-h6">Confirm Deletion</v-card-title>
      <v-card-text>
        <p>To confirm deletion, type the node template name: <strong>{{ nodeTemplate?.name }}</strong></p>
        <v-text-field
          v-model="deleteConfirmInput"
          label="Node Template name"
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
          :disabled="deleteConfirmInput !== nodeTemplate?.name"
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
import nodeTemplateService from '@/services/nodeTemplateService'
import Logbook from '@/components/Logbook.vue'
import { useAuthStore } from '@/stores/authStore'
import { useTextStore } from '@/stores/textStore'

const authStore = useAuthStore()
const textStore = useTextStore()
const nodeTemplateId = ref(useRoute().params.id)
const router = useRouter()
const nodeTemplate = ref(null)

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
const nodeTemplateToDelete = ref(null)
const deleteConfirmInput = ref('')
const protobuf_schema = ref('')
const configPreview = ref('')
// Fetch node template
nodeTemplateService.getNodeTemplate(nodeTemplateId.value)
  .then((data) => {
    nodeTemplate.value = data
    // Map the state property to an enum object definited in textstore that also contains a color and label value
    const matchedState = Object.values(textStore.nodeTemplateStatusEnum).find(
      s => s.name === data.state
    )
    nodeTemplate.value.state = {
      name: data.state,
      label: matchedState ? matchedState.label : data.state,
      color: matchedState ? matchedState.color : 'grey'
    }
    // sort configurables by type
    nodeTemplate.value.configurables.sort((a, b) => a.type.localeCompare(b.type))
    // build the config preview object
    for (const conf in nodeTemplate.value.configurables) {
      configPreview.value += `#define ${nodeTemplate.value.configurables[conf].name} <placeholder>\n`
    }
    // set commercial sensor as empty object instead of null
    nodeTemplate.value.fields.forEach((field) => {
      if (field.commercial_sensor === null) {
        field.commercial_sensor = {}
      }
    })
  })
  .catch((error) => {
    console.error(`Error fetching node template ${nodeTemplateId.value}:`, error)
  })
  .finally(() => loading.value = false)
// Fetch protobuff schema
nodeTemplateService.getNodeTemplateSchema(nodeTemplateId.value)
  .then((data) => {
    protobuf_schema.value = data
  })
  .catch((error) => {
    console.error(`Error fetching node template ${nodeTemplateId.value} schema:`, error)
  })


const deletenodeTemplate = (id) => {
  nodeTemplateToDelete.value = id
  deleteConfirmInput.value = ''
  confirmDelete.value = true
}

const performDelete = () => {
  nodeTemplateService.deleteNodeTemplate(nodeTemplateToDelete.value)
    .then(() => {
        confirmDelete.value = false
        router.push('/node-templates')
    })
    .catch(() => console.error(`Error deleting node template ${nodeTemplateToDelete.value}`))
}
const copySchema = () => {
  const schemaText = JSON.stringify(protobuf_schema.value, null, 2)
  navigator.clipboard.writeText(schemaText).catch(err => {
    console.error('Failed to copy schema: ', err)
  })
}
const openGitlabUrl = () => {
    window.open(nodeTemplate.value.gitlab_url, '_blank')
}
</script>