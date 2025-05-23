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
    <v-row v-if="jobStatus === 'successful'">
      <v-col cols="8">
        <v-btn
        color="secondary"
        class="mb-4"
        @click="downloadArtifacts"
        download

        >
            Download Artifacts
        </v-btn>
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

    <v-divider v-if="jobStatus === 'successful'" class="my-6"></v-divider>
    <!-- Flashing Section -->
    <v-row v-if="jobStatus === 'successful'">
      <v-col class="pa-4 mb-4">
        <h4 class="text-h6 mb-4">Flash ESP Board</h4>
        <v-btn
          v-if="isSerialConnected"
          color="primary"
          class="me-4 mb-2"
          @click="serialDisconnect"
          :disabled="isSerialFlashing"
        >
          Disconnect
        </v-btn>
        <v-btn
          v-else
          color="primary"
          class="me-4 mb-2"
          @click="serialConnect"
        >
          Connect
        </v-btn>
        <v-btn
            v-if="isSerialConnected"
            color="secondary"
            class="mb-2"
            @click="flashFirmware"
            :disabled="isSerialFlashing"
        >
            Flash Firmware
        </v-btn>
        <h4 class="mt-4 mb-2">ESP Tool logs</h4>
        <v-sheet
            style="background-color: #272822; color: #f8f8f2; font-family: monospace; white-space: pre; overflow: auto; border-radius: 8px; height: 200px;"
        >
            {{flashingLogs }}
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ESPLoader, Transport } from 'esptool-js'
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
const compilationLogs = ref('')
const jobId = ref('')
const jobStatus = ref('')
const flashingLogs = ref('')
const isSerialConnected = ref(false)
const isSerialFlashing = ref(false)
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

const downloadArtifacts = () => {
  compilationService.getBuildArtifact(
    jobId.value,
    downloadOptions.bin_only,
    downloadOptions.get_source_code,
    downloadOptions.get_logs,
    true
  )
  .then(artifact => {
    const blob = new Blob([artifact])
    const url = window.URL.createObjectURL(blob)

    const a = document.createElement('a')
    a.href = url
    a.download = 'firmware.bin'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  })
  .catch(error => {
    compilationLogs.value += `ERROR downloading artifact: ${error.message}\n`
  })
}
let SerialPort = null
let SerialTransport = null
let SerialLoader = null
let SerialChipRom = null
// Set up a terminal to funnel SerialLoader messages into our UI
const terminal = {
    clean() {},
    writeLine: (line) => { flashingLogs.value += line + '\n' },
    write: (data) => { flashingLogs.value += data }
}
// Function to connect to the serial SerialPort
const serialConnect = async () => {
  try {
    if(SerialPort === null) {
        // Prompt user to select a serial SerialPort
        SerialPort = await navigator.serial.requestPort()
        // Wrap the SerialPort in esptool-js Transport and open it
        SerialTransport = new Transport(SerialPort, true)
    }
    // Initialize the ESPLoader and perform the bootloader handshake
    SerialLoader = new ESPLoader({ transport: SerialTransport, baudrate: textStore.serialBaudrate, terminal })
    SerialChipRom = await SerialLoader.main()
    isSerialConnected.value = true
  } catch (error) {
    flashingLogs.value += `ERROR: ${error.message}\n`
    isSerialConnected.value = false
  }
}

// Function to disconnect from the serial SerialPort
const serialDisconnect = async () => {
  try {
    if (SerialTransport) {
      await SerialTransport.disconnect()
      flashingLogs.value += 'Transport disconnected.\n'
    }
  } catch (err) {
    flashingLogs.value += `ERROR during disconnect: ${err.message}\n`
  } finally {
    // Clean up references no matter what
    SerialPort = null
    SerialTransport = null
    SerialLoader = null
    SerialChipRom = null
    flashingLogs.value += 'Disconnected from ESP board.\n'
    isSerialConnected.value = false
    isSerialFlashing.value = false
  }
}

// Function to flash the firmware
const flashFirmware = async () => {
    isSerialFlashing.value = true
  try {
    if (!SerialLoader) {
      flashingLogs.value += 'ERROR: Board not connected. Please connect first.\n'
      return
    }
    flashingLogs.value += 'Fetching firmware binary...\n'
    // download compiled binary as ArrayBuffer
    const artifact = await compilationService.getBuildArtifact(jobId.value)
    const arrayBuffer = artifact
    const uint8 = new Uint8Array(arrayBuffer)
    // convert to binary string for esptool-js
    const firmwareStr = SerialLoader.ui8ToBstr(uint8)
    flashingLogs.value += 'Starting flash...\n'
    await SerialLoader.writeFlash({
      fileArray: [{ data: firmwareStr, address: 0x1000 }],
      flashSize: 'keep',
      eraseAll: false,
      compress: true,
      reportProgress: (fileIndex, written, total) => {
        flashingLogs.value += `Flashing ${(written/total*100).toFixed(1)}%...\n`
      }
    })
    await SerialLoader.after()
    flashingLogs.value += 'Flash completed successfully.\n'
    isSerialFlashing.value = false
  } catch (error) {
    flashingLogs.value += `ERROR during flash: ${error.message}\n`
    isSerialFlashing.value = false
  }
}
</script>