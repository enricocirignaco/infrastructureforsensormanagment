import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
  }),
  actions: {
    setToken(token) {
      this.token = token
    },
    clearToken() {
      this.token = null
    }
  },
  getters: {
    isAuthenticated: (state) => !!state.token,  // Returns true if token exists
    getAuthHeader: (header) => header['Authorization'] = 'Bearer ' + token, // Returns the authorization header with the token
  }
})