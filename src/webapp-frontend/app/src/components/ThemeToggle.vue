<template>
  <v-switch
    v-model="isDarkMode"
    label="Dark Mode"
    color="secondary"
    hide-details
    class="custom-switch"
    @change="toggleTheme"
  >
    <template v-slot:label>
      <v-icon v-if="isDarkMode">mdi-weather-sunny</v-icon>
      <v-icon v-else>mdi-moon-waning-crescent</v-icon>
    </template>
  </v-switch>
</template>

<script setup>
import { ref } from 'vue'
import { useSettingsStore } from '@/stores/settingsStore'
import { useTheme } from 'vuetify'

const theme = useTheme()
const settingsStore = useSettingsStore()
const isDarkMode = ref(settingsStore.isDarkMode)

// set right theme before loading the app
theme.global.name.value = settingsStore.isDarkMode ? 'dark' : 'light'
function toggleTheme() {
  settingsStore.toggleDarkMode()
  theme.global.name.value = settingsStore.isDarkMode ? 'dark' : 'light'
}
</script>

<style scoped>
.custom-switch {
  display: flex;
  justify-content: space-between;
  width: 80px;
  padding: 0;
}

.custom-switch .v-input__control {
  display: flex;
  align-items: center;
}

.custom-switch .v-input__control .v-icon {
  font-size: 20px;
  margin: 0 5px;
}

.v-switch {
  position: relative;
}

.v-switch .v-input__control .v-icon {
  position: absolute;
  transition: transform 0.2s ease-in-out;
}

.v-switch .v-input__control .v-icon:nth-child(1) {
  left: 5px;
}

.v-switch .v-input__control .v-icon:nth-child(2) {
  right: 5px;
}
</style>
