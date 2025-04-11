<template>
    <v-card>
        <v-card-title>Change Password</v-card-title>

        <!-- Password Change Form -->
        <v-form ref="passwordForm" @submit.prevent="submitPasswordForm">
            <v-text-field
                v-model="currentPassword"
                :type="showCurrentPassword ? 'text' : 'password'"
                label="Current Password"
                :append-inner-icon="showCurrentPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showCurrentPassword = !showCurrentPassword"
                autocomplete="current-password"
                required
                :rules="[v => !!v || 'Password is required']"
              />

            <v-text-field
                v-model="newPassword"
                :type="showNewPassword ? 'text' : 'password'"
                label="New Password"
                :append-inner-icon="showNewPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showNewPassword = !showNewPassword"
                autocomplete="new-password"
                required
                :rules="[v => !!v || 'New Password is required']"
            />

            <v-text-field
                v-model="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                label="Confirm New Password"
                :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showConfirmPassword = !showConfirmPassword"
                autocomplete="new-password"
                required
                :rules="[
                    v => !!v || 'Confirm Password is required',
                    v => v === newPassword || 'Passwords must match'
                ]"

            />

            <v-btn type="submit" color="primary">Submit</v-btn>
        </v-form>

        <!-- Error Messages -->
        <v-alert v-if="errorMessage" type="error" class="mt-4">{{ errorMessage }}</v-alert>
        <v-alert v-if="successMessage" type="success" class="mt-4">{{ successMessage }}</v-alert>

        <!-- New User Section (Visible for Admins only) -->
        <v-divider class="my-4"></v-divider>
        <v-card-title>Create New User</v-card-title>

        <v-form @submit.prevent="createNewUser">
            <v-text-field
                v-model="newUser.username"
                label="Username"
                required
            />
            <v-text-field
                v-model="newUser.fullname"
                label="Full Name"
                required
            />
            <v-select
                v-model="newUser.role"
                :items="roles"
                label="Role"
                required
            />

            <!-- Submit Button to create a new user -->
            <v-btn type="submit" color="primary">Create User</v-btn>
        </v-form>

        <!-- Display the randomly generated password for the new user -->
        <v-alert v-if="generatedPassword" type="info" class="mt-4">
            Generated Password: {{ generatedPassword }}
            <v-btn icon @click="copyPassword" class="ml-2">
                <v-icon>mdi-content-copy</v-icon>
            </v-btn>
        </v-alert>
    </v-card>
</template>

<script setup>
import { ref } from 'vue'
import userService from '@/services/userService'
import { useAuthStore } from '@/stores/authStore'
// State for password change
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const passwordForm = ref(null)
const authStore = useAuthStore()
// State for creating a new user (visible only for admins)
const newUser = ref({
  username: '',
  fullname: '',
  role: ''
})

const roles = ['Admin', 'User'] // Example roles for user creation
const generatedPassword = ref('')

// Handle form submission for personal password change
const submitPasswordForm = () => {
    // Validate the password change form
    if (currentPassword.value && newPassword.value && newPassword.value === confirmPassword.value) {
        // Update Password
        userService.patchUserPassword(authStore.getUserId(), currentPassword.value, newPassword.value)
            .then((token) => {
                authStore.setToken(token)
                console.log(userService.getUser(authStore.getUserId()))
                successMessage.value = 'Your password has been successfully changed.'
                errorMessage.value = ''
            })
            .catch((error) => {
                errorMessage.value = 'Failed to change password: ' + error.message
                successMessage.value = ''
            })

        passwordForm.value.reset()
        passwordForm.value.resetValidation()
    }
}

// Generate a random password for the new user
const generateRandomPassword = () => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let password = ''
  for (let i = 0; i < 8; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return password
}

// Handle user creation
const createNewUser = () => {
    if (newUser.value.username && newUser.value.fullname && newUser.value.role) {
        // Generate a random password for the new user
        generatedPassword.value = generateRandomPassword()

        // Simulate creating a new user (you can replace this with an actual API call)
        console.log('New user created:', newUser.value)

        // Reset the new user form
        newUser.value.username = ''
        newUser.value.fullname = ''
        newUser.value.role = ''
    } else {
        errorMessage.value = 'Please fill in all fields to create the user.'
    }
}

// Copy the password to the clipboard
const copyPassword = () => {
    navigator.clipboard.writeText(generatedPassword.value)
        .then(() => {
            successMessage.value = 'Password copied to clipboard!'
        })
        .catch(() => {
            errorMessage.value = 'Failed to copy password.'
        })
}
</script>

<style scoped>
.v-card {
  padding: 20px;
}

.v-btn {
  width: 100%;
}

.v-alert {
  text-align: center;
}

.my-4 {
  margin-top: 1rem;
  margin-bottom: 1rem;
}
</style>