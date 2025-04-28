import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') || null, // Load token from localStorage if it exists
  }),
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('auth_token', token) // Save token to localStorage
    },
    clearToken() {
      this.token = null
      localStorage.removeItem('auth_token') // Remove token from localStorage
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token, // Returns true if token exists
    getAuthHeader:
      (state) =>
      (header = {}) => {
        if (state.isAuthenticated) {
          // Assign the token to the Authorization header if it exists
          header['Authorization'] = 'Bearer ' + state.token
        }
        return header
      },
    getUser: (state) => {
      if (state.token) {
        try {
          let user = JSON.parse(atob(state.token.split('.')[1]))
          user.uuid = user.sub
          delete user.sub
          return user
        } catch {
          return null
        }
      }
      return null
    },
  },
})
