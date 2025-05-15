<template>
  <div style="height: 75vh; overflow: hidden;">
    <!-- Title -->
    <v-container class="pa-4">
      <v-row>
        <v-col cols="12">
          <h1 class="text-h5 mb-6">Welcome back, {{ authStore.getUser?.full_name || '' }}</h1>
        </v-col>
      </v-row>
    </v-container>
    <!-- Loading Animation -->
    <v-container class="fill-height pa-4">
      <v-row v-if="loading" class="fill-height justify-center align-center">
        <v-col cols="12" class="text-center">
          <v-progress-circular indeterminate size="64" color="primary" />
          <div class="mt-4">Loading Dashboard...</div>
        </v-col>
      </v-row>

      <template v-else>
        <v-row class="fill-height flex-wrap gap-4" align="stretch">
          <!-- Projects -->
          <v-col cols="6" class="d-flex" style="height: calc(50% - 12px);">
            <v-card
              class="d-flex flex-column justify-center align-center text-center"
              elevation="2"
              style="width: 100%; height: 100%"
              to="/projects"
              hover
              ripple
            >
              <v-card-title class="text-h6">Projects</v-card-title>
              
                <v-card-text>
                  <v-icon size="48" class="mb-2" :icon="textStore.icons.projects" /> 
                  <div class="text-h4 font-weight-bold mb-2">{{ projectsStats?.total ?? '-' }}</div>
                  <div class="text-subtitle-2">Projects Total</div>
                  <div class="text-caption mt-1">
                    {{ projectsStats?.active ?? '-' }} Active • {{ projectsStats?.archived ?? '-' }} Archived
                  </div>
                </v-card-text>
              
            </v-card>
          </v-col>
          <!-- Sensor nodes -->
          <v-col cols="6" class="d-flex" style="height: calc(50% - 12px);">
            <v-card
              class="d-flex flex-column justify-center align-center text-center"
              elevation="2"
              style="width: 100%; height: 100%"
              to="/sensor-nodes"
              hover
              ripple
            >
            <v-card-title class="text-h6">Sensor Nodes</v-card-title>
              <v-card-text>
                <v-icon size="48" class="mb-2" :icon="textStore.icons.sensorNodes" /> 
                <div class="text-h4 font-weight-bold mb-2">{{ sensorNodesStats.total }}</div>
                <div class="text-subtitle-2">Sensor Nodes</div>
                <div class="text-caption mt-1">{{sensorNodesStats.active}} Active • {{sensorNodesStats.inactive}} Inactive</div>
              </v-card-text>
            </v-card>
          </v-col>
          <!-- Commercial sensors -->
          <v-col cols="6" class="d-flex" style="height: calc(50% - 12px);">
            <v-card
              class="d-flex flex-column justify-center align-center text-center"
              elevation="2"
              style="width: 100%; height: 100%"
              to="/commercial-sensors"
              hover
              ripple
            >
              <v-card-title class="text-h6">Commercial Sensors</v-card-title>
              <v-card-text>
                <v-icon size="48" class="mb-2" :icon="textStore.icons.commercialSensors" />
                <div class="text-h4 font-weight-bold mb-2">{{ commercialSensorsStats?.total ?? '-' }}</div>
                <div class="text-subtitle-2">Commercial Sensors</div>
              </v-card-text>
            </v-card>
          </v-col>
          <!-- Node templates -->
          <v-col cols="6" class="d-flex" style="height: calc(50% - 12px);">
            <v-card
              class="d-flex flex-column justify-center align-center text-center"
              elevation="2"
              style="width: 100%; height: 100%"
              to="/node-templates"
              hover
              ripple
            >
              <v-card-title class="text-h6">Node Templates</v-card-title>
              <v-card-text>
                <v-icon size="48" class="mb-2" :icon="textStore.icons.nodeTemplates" /> 
                <div class="text-h4 font-weight-bold mb-2">{{ nodeTemplatesStats.total }}</div>
                <div class="text-subtitle-2">Node Templates</div>
                <div class="text-caption mt-1">{{nodeTemplatesStats.inUse}} In Use • {{nodeTemplatesStats.archived}} Archived</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import projectService from '@/services/projectService'
import commercialSensorService from '@/services/commercialSensorService'
import { ref } from 'vue'
import { useTextStore } from '@/stores/textStore'
import nodeTemplateService from '@/services/nodeTemplateService'
import sensorNodeService from '@/services/sensorNodeService'
const textStore = useTextStore()
const authStore = useAuthStore()
let projectsStats = ref(null)
let commercialSensorsStats = ref(null)
const nodeTemplatesStats = ref(null)
const sensorNodesStats = ref(null)
const loading = ref(true)

Promise.all([
  projectService.getProjectsDTO()
    .then((projectsDTO) => {
      if (!projectsDTO) return Promise.reject('No projects data found')
      projectsStats.value = {
        total: projectsDTO.length,
        active: projectsDTO.filter(project => project.state === 'Active').length,
        archived: projectsDTO.filter(project => project.state === 'Archived').length,
      }
    }),
  commercialSensorService.getCommercialSensorsDTO()
    .then((commercialSensorsDTO) => {
      if (!commercialSensorsDTO) return Promise.reject('No commercial sensors data found')
      commercialSensorsStats.value = {
        total: commercialSensorsDTO.length
      }
    }),
  nodeTemplateService.getNodeTemplatesDTO()
    .then((nodeTemplatesDTO) => {
      if (!nodeTemplatesDTO) return Promise.reject('No node templates data found')
      nodeTemplatesStats.value = {
        total: nodeTemplatesDTO.length,
        inUse: nodeTemplatesDTO.filter(template => template.state === 'In-Use').length,
        archived: nodeTemplatesDTO.filter(template => template.state === 'Archived').length,
      }
    }),
  sensorNodeService.getSensorNodesDTO()
    .then((sensorNodesDTO) => {
      if (!sensorNodesDTO) return Promise.reject('No sensor nodes data found')
      sensorNodesStats.value = {
        total: sensorNodesDTO.length,
        active: sensorNodesDTO.filter(node => node.state === 'Active').length,
        inactive: sensorNodesDTO.filter(node => node.state === 'Inactive').length,
      }
    }),
])
  .catch((error) => {
    console.error('Error loading dashboard data:', error)
  })
  .finally(() => {
    loading.value = false
  })
</script>