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
            ref="compilationLogSheet"
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
          :disabled="downloadOptions.get_source_code || downloadOptions.get_logs"
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
          :disabled="downloadOptions.bin_only"
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
          :disabled="downloadOptions.bin_only"
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
          :disabled="isConsoleConnected"
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
            elevation="1"
            class="pa-4 position-relative"
            style="background-color: #272822; color: #f8f8f2; font-family: monospace; white-space: pre; overflow: auto; border-radius: 8px; height: 200px;"
            ref="flashingLogsSheet"
            >
            {{flashingLogs }}
        </v-sheet>
      </v-col>
    </v-row>
    <!-- Serial Console Section -->
    <v-row>
      <v-col class="pa-4 mb-4">
        <h4 class="text-h6 mb-4">Serial Console</h4>
        <v-btn
          v-if="isConsoleConnected"
          color="primary"
          class="me-4 mb-2"
          @click="serialConsoleDisconnect"
          :disabled="isSerialConnected"
        >
          Disconnect
        </v-btn>
        <v-btn
          v-else
          color="primary"
          class="me-4 mb-2"
          @click="serialConsoleConnect"
          :disabled="isSerialConnected"
        >
          Connect
        </v-btn>
        <!-- <h4 class="mt-4 mb-2">ESP Tool logs</h4> -->
        <v-sheet
            elevation="1"
            class="pa-4 position-relative"
            style="background-color: #272822; color: #f8f8f2; font-family: monospace; white-space: pre; overflow: auto; border-radius: 8px; height: 200px;"
            ref="consoleLogsSheet"
            >
            {{consoleLogs }}
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
import { watch, nextTick } from 'vue'

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
const isConsoleConnected = ref(false)
const isSerialFlashing = ref(false)
const compilationLogSheet = ref(null)
const flashingLogsSheet = ref(null)
const consoleLogsSheet = ref(null)
const consoleLogs = ref('')
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
    downloadOptions.get_logs
  )
  .then(response => {
    const disposition = response.headers.get('Content-Disposition');
    const match = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(disposition);
    const filename = match ? match[1].replace(/['"]/g, '') : 'firmware.bin';

    return response.blob().then(blob => ({ blob, filename }));
  })
  .then(({ blob, filename }) => {
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  })
  .catch(error => {
    compilationLogs.value += `ERROR downloading artifact: ${error.message}\n`;
  });
}

// Scroll to the bottom of the logs when any of them change
;[compilationLogs, flashingLogs, consoleLogs].forEach((logRef, i) => {
  const sheetRef = [compilationLogSheet, flashingLogsSheet, consoleLogsSheet][i]
  watch(logRef, () => {
    nextTick(() => {
      const el = sheetRef.value?.$el || sheetRef.value
      if (el) el.scrollTop = el.scrollHeight
    })
  })
})


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
// serial console connection
let reader = null
const serialConsoleConnect = async () => {
  try {
    if(SerialPort === null){
      SerialPort = await navigator.serial.requestPort()
      await SerialPort.open({ baudRate: textStore.serialBaudrate })
      SerialTransport = new Transport(SerialPort)
      consoleLogs.value += 'Triggering a DTR reset...\n'
      await SerialTransport.setDTR(false)
      await new Promise(r => setTimeout(r, 100))
      await SerialTransport.setDTR(true)
    }
    const decoder = new TextDecoder()
    reader = SerialPort.readable.getReader()
    isConsoleConnected.value = true
    consoleLogs.value += `Serial console connected at ${textStore.serialBaudrate} baud\n`

    // Read loop: append incoming data to logs
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value)
      consoleLogs.value += chunk
    }
  } catch (error) {
    consoleLogs.value += `ERROR in serial console: ${error.message}\n`
    reader?.releaseLock()
    isConsoleConnected.value = false
  }
}
// serial console disconnection
const serialConsoleDisconnect = async () => {
  try {
    if (SerialPort && reader) {
      // Release reader when done
      reader.releaseLock()
      await SerialPort.close()
      consoleLogs.value += 'Serial console disconnected.\n'
    }
  } catch (err) {
    consoleLogs.value += `ERROR during console disconnect: ${err.message}\n`
  } finally {
    SerialPort = null
    SerialTransport = null
    reader = null
    isConsoleConnected.value = false
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
    const response = await compilationService.getBuildArtifact(jobId.value)
    flashingLogs.value += 'Firmware binary fetched successfully.\n'
    const blob = await response.blob()
    const arrayBuffer = await blob.arrayBuffer()
    const uint8Array = new Uint8Array(arrayBuffer)
    const firmwareStr = SerialLoader.ui8ToBstr(uint8Array)
    flashingLogs.value += 'Starting flash...\n'
    await SerialLoader.writeFlash({
      fileArray: [{ data: firmwareStr, address: 0x0000 }],
      flashSize: 'keep',
      eraseAll: false,
      compress: true,
      reportProgress: (fileIndex, written, total) => {
        flashingLogs.value += `Flashing ${(written/total*100).toFixed(1)}%...\n`
      }
    })
    await SerialLoader.after()
    flashingLogs.value += 'Flash completed successfully.\n'
  } catch (error) {
    flashingLogs.value += `ERROR during flash: ${error.message}\n`
  }
  finally {
    isSerialFlashing.value = false
  }
}
</script>