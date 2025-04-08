<template>
  <v-app>
    <v-main>
      <v-container class="d-flex justify-center align-center" style="height: 100vh;">
        <v-card width="400" class="mx-auto mt-5">
          <v-card-title class="text-h5 text-center">Login</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="submit">
              <v-text-field
                v-model="username"
                label="Username"
                prepend-icon="mdi-account"
                required
                autocomplete="username"
              />

              <v-text-field
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                label="Password"
                prepend-icon="mdi-lock"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                required
                autocomplete="current-password"
              />

            </v-form>
          </v-card-text>
          <v-divider></v-divider>
            <v-card-actions>
              <v-btn color="success">Register</v-btn>
              <v-btn color="info">Login</v-btn>
            </v-card-actions>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const password = ref('')
const showPassword = ref(false)

function submit() {
  console.log('Login:', { username: username.value, password: password.value })
}

function register() {
  console.log('Go to registration page')
}
</script>

<style scoped>
.v-input__append-inner .v-icon {
  color: rgba(0, 0, 0, 0.6); /* adjust for visibility */
  cursor: pointer;
}
</style>