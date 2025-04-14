import { defineStore } from 'pinia'

export const useTextStore = defineStore('text', {
  state: () => ({
    sloganMultiLine: 'Innovating Nature-Care<br>with Smart Technology',
    slogan: 'Innovating Nature-Care with Smart Technology',
    applicationName: 'Internet of Soils',
    restApiBaseUrl: 'https://api.example.com',
  }),
})
