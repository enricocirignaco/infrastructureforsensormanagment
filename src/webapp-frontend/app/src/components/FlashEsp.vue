<template>
  <v-container>
    <!-- Compilation Section -->
    <v-row>
      <v-col>
            <v-btn
            :disabled="jobStatus === 'running' || jobStatus === 'pending'"
            color="secondary"
            class="mb-2"
            @click="triggerCompilation"
            >
            Compile Firmware</v-btn>
            <span v-if="jobId" class="ms-4 text-caption">Job ID: {{ jobId }}</span>
            <h4 class="mb-2">Compiler engine logs</h4>
            <v-sheet
                elevation="1"
                class="pa-4 position-relative"
                style="background-color: #272822; color: #f8f8f2; font-family: monospace; white-space: pre; overflow: auto; border-radius: 8px; height: 200px;"
                >
                {{ compilationLogs }}
            </v-sheet>
      </v-col>
    </v-row>

    <!-- Artifact Download Section -->
    <v-row v-if="jobStatus === 'success'">
      <v-col cols="8">
        <v-btn
        color="secondary"
        class="mb-4"
        :href="`/compilation/job/${jobId}/artifacts?bin_only=${downloadOptions.bin_only}&get_source_code=${downloadOptions.get_source_code}&get_logs=${downloadOptions.get_logs}`"
        download
        >
        Download Artifacts</v-btn>
      </v-col>

      <v-col cols="4">
         <v-switch
          v-model="downloadOptions.bin_only"
          label="Binary Only"
          inset
          hide-details
          density="comfortable"
          class="rounded-pill mb-2"
          style="transform: scale(0.85); height: 32px;"
          color="secondary"
        ></v-switch>

        <v-switch
          v-model="downloadOptions.get_source_code"
          label="Include Source Code"
          inset
          hide-details
          density="comfortable"
          class="rounded-pill mb-2"
          style="transform: scale(0.85); height: 32px;"
          color="secondary"
        ></v-switch>

        <v-switch
          v-model="downloadOptions.get_logs"
          label="Include Logs"
          inset
          hide-details
          density="comfortable"
          class="rounded-pill"
          style="transform: scale(0.85); height: 32px;"
          color="secondary"
        ></v-switch>
      </v-col>
    </v-row>

    <v-divider class="my-6"></v-divider>
    <!-- Flashing Section -->
    <v-row v-if="isCompilationSuccess">
      <v-col class="pa-4 mb-4">
        <h4 class="text-h6 mb-4">Flash ESP Board</h4>
        <v-btn color="primary" class="me-4 mb-2">Connect</v-btn>
        <v-btn
            color="primary"
            class="mb-2"
            @click="connectAndFlash"
        >
            Flash ESP
        </v-btn>
        <h4 class="mt-4 mb-2">ESP Tool logs</h4>
        <v-sheet
            style="background-color: #272822; color: #f8f8f2; font-family: monospace; white-space: pre; overflow: auto; border-radius: 8px; max-height: 300px; min-height: 100px;"
        >
            {{ }}
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>

import { reactive, ref } from 'vue'
import { ESPLoader } from 'esptool-js'
import { useTextStore } from '@/stores/textStore'
import compilationService from '@/services/compilationService'

const downloadOptions = reactive({
  bin_only: true,
  get_source_code: false,
  get_logs: false
})

const { sensorId } = defineProps({
  sensorId: {
    type: String,
    default: null
  }
})

const textStore = useTextStore()
const isCompilationSuccess = ref(true)
const compilationLogs = ref('')
const jobId = ref('')
const jobStatus = ref('')

// Function to start the compilation process
const triggerCompilation = () => {
  compilationService.buildFirmware(sensorId)
    .then((response) => {
      compilationLogs.value +=
        response.status.toUpperCase() + ' - ' + new Date(response.timestamp).toLocaleString() + ':    ' + response.message + '\n'
      jobId.value = response.job_id
      jobStatus.value = response.status
      startPolling()
    })
    .catch((error) => {
      compilationLogs.value += 'ERROR:' + error.message + '\n'
    })
}
// Start polling for compilation status
const startPolling = () => {
  const poll = () => {
    if (jobStatus.value === 'pending' || jobStatus.value === 'running') {
      setTimeout(() => {
        checkCompilationStatus().then(poll)
      }, textStore.compilationPollingInterval)
    }
  }
  poll()
}
// Function to check the compilation status
const checkCompilationStatus = () => {
  return compilationService.getBuildJobStatus(jobId.value)
    .then((response) => {
      const timestamp = new Date().toLocaleString()
      compilationLogs.value +=
        response.status.toUpperCase() + ' - ' + timestamp + ':    ' + response.message + '\n'
      jobStatus.value = response.status
    })
    .catch((error) => {
      compilationLogs.value += 'ERROR:' + error.message + '\n'
    })
}




// Example stub function
const connectAndFlash = async () => {
  const port = await navigator.serial.requestPort()
  const transport = new ESPLoader.SerialTransport(port)
  const loader = new ESPLoader(transport, 'esp32') // adjust chip type

  await loader.initialize()
  // loader.flashData(...) // to be added
}
</script>