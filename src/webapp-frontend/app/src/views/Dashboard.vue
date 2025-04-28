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
              <v-icon size="48" class="mb-2">mdi-folder</v-icon>
              <div class="text-h4 font-weight-bold mb-2">12</div>
              <div class="text-subtitle-2">Projects Total</div>
              <div class="text-caption mt-1">5 Active • 3 Updated</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" class="d-flex" style="height: calc(50% - 12px);">
          <v-card
            class="d-flex flex-column justify-center align-center text-center"
            elevation="2"
            style="width: 100%; height: 100%"
            to="/commercial-sensor"
            hover
            ripple
          >
            <v-card-title class="text-h6">Commercial Sensors</v-card-title>
            <v-card-text>
              <v-icon size="48" class="mb-2">mdi-chip</v-icon>
              <div class="text-h4 font-weight-bold mb-2">24</div>
              <div class="text-subtitle-2">Commercial Sensors</div>
              <div class="text-caption mt-1">8 Vendors • 2 Pending</div>
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
              <v-icon size="48" class="mb-2">mdi-wifi</v-icon>
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
            <v-card-title class="text-h6">Sensor Templates</v-card-title>
            <v-card-text>
              <v-icon size="48" class="mb-2">mdi-file-document-multiple</v-icon>
              <div class="text-h4 font-weight-bold mb-2">15</div>
              <div class="text-subtitle-2">Sensor Templates</div>
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

const authStore = useAuthStore()

</script>