<template>
  <v-container>
    <!-- Compilation Section -->
    <v-row>
      <v-col>
            <v-btn color="secondary" class="mb-2">Compile Firmware</v-btn>
            <h4 class="mb-2">Compiler engine logs</h4>
            <v-sheet
                style="background-color: #272822; color: #f8f8f2; font-family: monospace; white-space: pre; overflow: auto; border-radius: 8px; max-height: 300px; min-height: 100px;"
            >
                {{ configPreview }}
            </v-sheet>
      </v-col>
    </v-row>

    <!-- Artifact Download Section -->
    <v-row v-if="isCompilationSuccess">
      <v-col cols="8">
        <v-btn color="secondary" class="mb-4">Download Artifacts</v-btn>
      </v-col>

      <v-col cols="4">
        <v-switch
          v-model="hideInactive"
          label="Binary Only"
          inset
          hide-details
          density="comfortable"
          class="rounded-pill mb-2"
          style="transform: scale(0.85); height: 32px;"
          color="secondary"
        ></v-switch>

        <v-switch
          v-model="hideInactive"
          label="Include Source Code"
          inset
          hide-details
          density="comfortable"
          class="rounded-pill mb-2"
          style="transform: scale(0.85); height: 32px;"
          color="secondary"
        ></v-switch>

        <v-switch
          v-model="hideInactive"
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
            {{ configPreview }}
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { ESPLoader } from 'esptool-js'
import { useTextStore } from '@/stores/textStore'

const textStore = useTextStore()
const isCompilationDone = ref(true)
const isCompilationSuccess = ref(true)
const downloadOptions = ref([])
// Example stub function
const connectAndFlash = async () => {
  const port = await navigator.serial.requestPort()
  const transport = new ESPLoader.SerialTransport(port)
  const loader = new ESPLoader(transport, 'esp32') // adjust chip type

  await loader.initialize()
  // loader.flashData(...) // to be added
}
</script>