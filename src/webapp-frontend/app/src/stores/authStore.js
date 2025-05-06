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
    ensureValidToken() {
      // delete token if expired
      if (!this.isTokenValid) {
        this.clearToken()
        console.log('Token deleted')
        return false
      }
      return true
    },
    getAuthHeader(header = {}) {
      if (this.ensureValidToken()) {
        header['Authorization'] = 'Bearer ' + this.token
      }
      return header
    },
  },
  getters: {
    isTokenValid: (state) => {
      if (state.token) {
        try {
          // Decode the token and check its expiration
          const payload = JSON.parse(atob(state.token.split('.')[1]))
          if (typeof payload.exp !== 'number') return false
          const exp = payload.exp * 1000 // Convert to milliseconds
          return exp > Date.now() // Check if the token is still valid
        } catch (e) {
          console.error('Invalid token:', e)
          return false
        }
      }
      return false
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
