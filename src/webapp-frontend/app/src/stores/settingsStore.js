import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    // Parse the value to a boolean from localStorage
    isDarkMode: JSON.parse(localStorage.getItem('dark_mode')) || false,
  }),
  actions: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode
      // Save the boolean value back to localStorage
      localStorage.setItem('dark_mode', JSON.stringify(this.isDarkMode))
    },
  },
})
