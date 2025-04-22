<template>
    <v-container>
      <!-- Title & Button -->
      <v-row class="justify-space-between mb-4">
        <v-col cols="auto">
          <h1>Sensors</h1>
        </v-col>
        <v-col cols="auto">
        <v-btn rounded="xl" class="text-none" @click="router.push('/commercial-sensor/new')">
          <v-icon start>mdi-plus</v-icon>
          New Sensor
        </v-btn>
        </v-col>
      </v-row>
      <!-- Table -->
      <v-data-table
        :items="sensors"
        :headers="headers"
        @click:row="(_, { item }) => router.push(`/commercial-sensor/${item.id}`)"
        class="elevation-1 rounded-lg"
        hover
        rounded="lg"
        elevation="1"
        :loading="loading"
      >
      </v-data-table>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import commercialSensorService from '@/services/commercialSensorService'

  const router = useRouter()
  const sensors = ref([])
  const headers = [
    { title: 'Name', key: 'name' },
    { title: 'Alias', key: 'alias' },
    { title: 'Sensor ID', key: 'id' }
  ]
  const loading = ref(true)
  // Fetch sensors data
  commercialSensorService.getCommercialSensorsDTO()
    .then((data) => sensors.value = data)
    .catch((error) => {
      // TODO: Handle error
      console.error('Error fetching commercial sensors:', error)
    })
    .finally(() => loading.value = false)
  </script>
  