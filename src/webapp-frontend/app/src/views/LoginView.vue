<template>
  <v-app
    style="
      background-image: url('/images/login.jpg');
      background-size: cover;
      background-position: center;
    "
  >
    <v-main>
      <v-container class="d-flex justify-center align-center" style="height: 100vh">
        <v-card class="rounded-lg" width="400" elevation="10" color="primary">
          <!-- Logo -->
          <v-card-title class="text-center">
            <v-img src="/images/logo.svg" alt="Logo" height="100" />
          </v-card-title>

          <!-- Slogan -->
          <v-card-subtitle class="text-center mb-4">
            <span v-html="textStore.sloganMultiLine"></span>
          </v-card-subtitle>

          <!-- Form -->
          <v-card-text>
            <v-form ref="loginForm" @submit.prevent="submit">
              <!-- Display error message if login fails -->
              <v-alert v-if="loginError" type="error" class="mb-4">
                {{ loginError }}
              </v-alert>
              <v-text-field
                v-model="username"
                label="Username"
                prepend-icon="mdi-account"
                required
                autocomplete="username"
                :rules="[(v) => !!v || 'Username is required']"
              />
              <v-text-field
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                label="Password"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
                prepend-icon="mdi-lock"
                autocomplete="current-password"
                required
                :rules="[(v) => !!v || 'Password is required']"
              />
              <v-btn type="submit" color="secondary" block class="my-2">Login</v-btn>
              <v-btn variant="outlined" color="secondary" block @click="register">Register</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTextStore } from '@/stores/textStore'
import { useAuthStore } from '@/stores/authStore'
import authService from '@/services/authService'

const router = useRouter()
const textStore = useTextStore()
const authStore = useAuthStore()
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loginError = ref(null)

// Submit function to handle login
function submit() {
  if (username.value && password.value) {
    // Perform login action
    const user = {
      username: username.value,
      password: password.value,
    }
    authService
      .getAuthToken(user)
      .then((response) => {
        // Store the token in the auth store
        authStore.setToken(response.access_token)
        router.push('/')
      })
      .catch((error) => { 
        loginError.value = error.detail || 'Login failed. Please try again.'
      })
  }
}

// Register function to handle user registration
function register() {
  // TODO: Implement registration logic
  console.log('Go to registration page')
}
</script>
