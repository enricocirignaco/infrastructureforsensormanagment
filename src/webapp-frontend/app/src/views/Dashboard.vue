<template>
  <div style="height: 75vh; overflow: hidden;">
    <v-container class="pa-4">
      <v-row>
        <v-col cols="12">
          <h1 class="text-h5 mb-6">Welcome back, {{ authStore.getUser?.full_name || '' }}</h1>
        </v-col>
      </v-row>
    </v-container>

    <v-container class="fill-height pa-4">
      <v-row class="fill-height flex-wrap gap-4" align="stretch">
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
                <div class="text-h4 font-weight-bold mb-2">{{ projectsStats?.total ?? -1 }}</div>
                <div class="text-subtitle-2">Projects Total</div>
                <div class="text-caption mt-1">
                  {{ projectsStats?.active ?? -1 }} Active • {{ projectsStats?.updated ?? -1 }} Updated
                </div>
              </v-card-text>
            
          </v-card>
        </v-col>
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
              <v-icon size="48" class="mb-2" :icon="textStore.icons.commercialSensors" />              <div class="text-h4 font-weight-bold mb-2">{{ commercialSensorsStats?.total ?? -1 }}</div>
              <div class="text-subtitle-2">Commercial Sensors</div>
              <div class="text-caption mt-1">8 Vendors • {{ commercialSensorsStats?.total ?? -1 }} In Use</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" class="d-flex" style="height: calc(50% - 12px);">
          <v-card
            class="d-flex flex-column justify-center align-center text-center"
            elevation="2"
            style="width: 100%; height: 100%"
            to="/sensor-node"
            hover
            ripple
          >
            <v-card-title class="text-h6">Sensor Nodes</v-card-title>
            <v-card-text>
              <v-icon size="48" class="mb-2" :icon="textStore.icons.sensorNodes" /> 
              <div class="text-h4 font-weight-bold mb-2">40</div>
              <div class="text-subtitle-2">Sensor Nodes</div>
              <div class="text-caption mt-1">36 Online • 4 Offline</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" class="d-flex" style="height: calc(50% - 12px);">
          <v-card
            class="d-flex flex-column justify-center align-center text-center"
            elevation="2"
            style="width: 100%; height: 100%"
            to="/sensor-template"
            hover
            ripple
          >
            <v-card-title class="text-h6">Node Templates</v-card-title>
            <v-card-text>
              <v-icon size="48" class="mb-2" :icon="textStore.icons.nodeTemplates" /> 
              <div class="text-h4 font-weight-bold mb-2">15</div>
              <div class="text-subtitle-2">Node Templates</div>
              <div class="text-caption mt-1">9 Used • 6 Unused</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import projectService from '@/services/projectService'
import commercialSensorService from '@/services/commercialSensorService'
import { ref } from 'vue'
import { useTextStore } from '@/stores/textStore'

const textStore = useTextStore()
const authStore = useAuthStore()
let projectsStats = ref(null)
let commercialSensorsStats = ref(null)



// Fetch projects data
projectService.getProjectsDTO()
  .then((projectsDTO) => {
    if (!projectsDTO) return Promise.reject('No projects data found')
    projectsStats.value = {
      total: projectsDTO.length,
      active: projectsDTO.filter(project => project.state === 'Active').length,
      updated: projectsDTO.filter(project => project.updated).length,
    }
    })
  .catch((error) => {
    console.error('Error fetching projects:', error)
  })
// Fetch commercial sensor data
commercialSensorService.getCommercialSensorsDTO()
  .then((commercialSensorsDTO) => {
    if (!commercialSensorsDTO) return Promise.reject('No commercial sensors data found')
    commercialSensorsStats.value = {
      total: commercialSensorsDTO.length,
      active: commercialSensorsDTO.filter(sensor => sensor.state === 'Active').length,
      updated: commercialSensorsDTO.filter(sensor => sensor.updated).length,
    }
  })
  .catch((error) => {
    console.error('Error fetching commercial sensors:', error)
  })
</script>