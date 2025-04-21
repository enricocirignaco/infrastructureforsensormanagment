import { defineStore } from 'pinia'

export const useTextStore = defineStore('text', {
  state: () => ({
    sloganMultiLine: 'Innovating Nature-Care<br>with Smart Technology',
    slogan: 'Innovating Nature-Care with Smart Technology',
    applicationName: 'Internet of Soils',
    restApiBaseUrl: 'https://api.example.com',
    statusEnum: {
      0: 'Active',
      1: 'Archived',
      2: 'Deleted',
    },
    externalResourceTypeEnum: {
      0: 'Website',
      1: 'MS Teams',
      2: 'Report',
      3: 'Documentation',
      4: 'Misc',
    },
  }),
})