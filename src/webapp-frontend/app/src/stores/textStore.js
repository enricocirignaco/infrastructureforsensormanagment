import { defineStore } from 'pinia'

export const useTextStore = defineStore('text', {
  state: () => ({
    slogan: "Innovating Nature-Care<br>with Smart Technology"
  })
})