<template>
    <v-container v-if="loading" class="d-flex justify-center align-center" style="min-height: 300px">
      <v-progress-circular indeterminate color="primary" size="64" />
    </v-container>
    <v-container v-else>
      <v-row>
        <v-col cols="9">
          <!-- Sensor Details -->
          <v-card class="mb-4" rounded="lg">
            <v-card-title>
              <v-row class="w-100 align-center">
                  <!-- back button -->
                  <v-col cols="auto">
                      <v-btn icon @click="router.push('/commercial-sensors')">
                          <v-icon>mdi-arrow-left</v-icon>
                      <v-icon>mdi-arrow-left</v-icon>
                      </v-btn>
                  </v-col>
                  <!-- title -->
                  <v-col>
                      <h2 class="mb-0">{{ sensor.name }} - {{ sensor.alias }}</h2>
                  </v-col>
                  <!-- status & edit button -->
                  <v-col cols="auto" class="d-flex align-center">
                      <v-btn v-if="authStore.getUser?.role !== 'Researcher'" color="primary" icon size="small" class="me-1" @click="router.push(`/commercial-sensor/${sensorId}/edit`)">
                        <v-icon>mdi-pencil</v-icon>
                      </v-btn>
                      <v-btn v-if="authStore.getUser?.role !== 'Researcher'" color="error" icon size="small" @click="deleteSensor(sensorId)">
                        <v-icon>mdi-delete</v-icon>
                      </v-btn>
                  </v-col>
              </v-row>
            </v-card-title>
            <v-divider class="my-6" />
            <!-- sensor content -->
            <v-card-text>
              <div class="mb-6">
                <h3 class="text-h6 mb-2">Sensor Description</h3>
                <p class="text-body-1">{{ sensor.description }}</p>
              </div>
              <h3 class="text-h6 mb-2">Sensor Resources</h3>
              <!-- external props table -->
              <v-data-table
                :items="sensor.external_props"
                :headers="externalPropsHeaders"
                density="compact"
                class="rounded-lg elevation-1"
                hide-default-footer
                :group-by="groupBy"
                rounded="lg"
                elevation="1"
                show-group-by
              >
                <template #item.url="{ item }">
                  <a :href="item.url" target="_blank">{{ item.url }}</a>
                </template>
              </v-data-table>
                <v-divider class="my-6" />
                <!-- sensor props table -->
                <h3 class="text-h6 mb-2">Sensor Specifications</h3>
                <v-data-table
                    :items="sensor.sensor_props"
                    :headers="sensorPropsHeaders"
                    class="elevation-1 rounded-lg"
                    density="compact"
                    rounded="lg"
                    elevation="1"
                    hide-default-footer
                >
                  <template #item.precision="{ item }">
                    <span v-if="item.precision">
                      ± {{ item.precision }} {{ item.unit }}
                    </span>
                  </template>
                  <template #item.range.min="{ item }">
                    <span v-if="item.range.min !== undefined && item.range.min !== null">
                      {{ item.range.min }} {{ item.unit }}
                    </span>
                  </template>
                  <template #item.range.max="{ item }">
                    <span v-if="item.range.max !== undefined && item.range.max !== null">
                      {{ item.range.max }} {{ item.unit }}
                    </span>
                  </template>
                </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="3">
          <Logbook :logbook="sensor.logbook" />
        </v-col>
      </v-row>
    </v-container>
  
    <v-dialog v-model="confirmDelete" max-width="500">
      <v-card>
        <v-card-title class="text-h6">Confirm Deletion</v-card-title>
        <v-card-text>
          <p>To confirm deletion, type the sensor name: <strong>{{ sensor?.name }}</strong></p>
          <v-text-field
            v-model="deleteConfirmInput"
            label="Sensor name"
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
            :disabled="deleteConfirmInput !== sensor?.name"
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
  import commercialSensorService from '@/services/commercialSensorService'
  import Logbook from '@/components/Logbook.vue'
  import { useAuthStore } from '@/stores/authStore'

  const authStore = useAuthStore()
  const sensorId = ref(useRoute().params.id)
  const router = useRouter()
  const sensor = ref(null)
  const externalPropsHeaders = [
      { title: 'Name', key: 'name' },
      { title: 'URL', key: 'url' }
  ]
  const sensorPropsHeaders = [
    { title: 'Name', key: 'name', sortable: false},
    { title: 'Unit', key: 'unit' , sortable: false},
    { title: 'Precision', key: 'precision' , sortable: false},
    { title: 'Range', align: 'center', sortable: false,
      children: [
        { title: 'Min', key: 'range.min', sortable: false},
        { title: 'Max', key: 'range.max', sortable: false}
      ]
    }
  ]
  const groupBy = ref([{ key: 'type', order: 'asc' }])
  const loading = ref(true)
  const confirmDelete = ref(false)
  const sensorToDelete = ref(null)
  const deleteConfirmInput = ref('')
  
  // Fetch sensor data
  commercialSensorService.getCommercialSensor(sensorId.value)
      .then((data) => sensor.value = data)
      .catch((error) => {
        // TODO: Handle error
        console.error(`Error fetching commercial sensor ${sensorId.value}:`, error)
        })
        .finally(() => loading.value = false)
  // render status color
  function getStatusColor (status) {
      if (status === 'Active') return 'success'
      else if (status === 'Archived') return 'warning'
      else if (status === 'Deleted') return 'error'
      else return 'grey'
  }
  
  const deleteSensor = (id) => {
    sensorToDelete.value = id
    deleteConfirmInput.value = ''
    confirmDelete.value = true
  }
  
  const performDelete = () => {
    commercialSensorService.deleteCommercialSensor(sensorToDelete.value)
      .then(() => {
          router.push('/commercial-sensors')
          confirmDelete.value = false
      })
      .catch(() => console.error(`Error deleting commercial sensor ${sensorToDelete.value}`))
  }
  </script>