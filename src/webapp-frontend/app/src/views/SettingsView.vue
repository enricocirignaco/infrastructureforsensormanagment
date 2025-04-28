<template>
  <v-card>
    <v-card-title>Change Password</v-card-title>

    <!-- Password Change Form -->
    <v-form ref="passwordForm" @submit.prevent="submitPasswordForm">
      <!-- Needed for autofill functionality -->
      <input type="text" name="username" autocomplete="username" hidden />
      <v-text-field
        v-model="currentPassword"
        :type="showCurrentPassword ? 'text' : 'password'"
        label="Current Password"
        :append-inner-icon="showCurrentPassword ? 'mdi-eye-off' : 'mdi-eye'"
        @click:append-inner="showCurrentPassword = !showCurrentPassword"
        autocomplete="current-password"
        required
        :rules="[(v) => !!v || 'Password is required']"
      />

      <v-text-field
        v-model="newPassword"
        :type="showNewPassword ? 'text' : 'password'"
        label="New Password"
        :append-inner-icon="showNewPassword ? 'mdi-eye-off' : 'mdi-eye'"
        @click:append-inner="showNewPassword = !showNewPassword"
        autocomplete="new-password"
        required
        :rules="[(v) => !!v || 'New Password is required']"
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
          (v) => !!v || 'Confirm Password is required',
          (v) => v === newPassword || 'Passwords must match',
        ]"
      />
      <v-btn type="submit" color="primary">Submit</v-btn>
    </v-form>

    <!-- Error Messages -->
    <v-alert v-if="errorMessage" type="error" class="mt-4">{{ errorMessage }}</v-alert>
    <v-alert v-if="successMessage" type="success" class="mt-4">{{ successMessage }}</v-alert>
  </v-card>

<!-- Admin Only Section -->
  <v-container v-if="authStore.getUser?.role === 'Admin'">
    <v-divider class="my-4"></v-divider>
    <v-card-title>Admin Section</v-card-title>
    <v-divider class="my-4"></v-divider>
    <!-- Create new user section-->
    <v-card>
      <v-card-title>Create New User</v-card-title>
      <v-card>
        <v-form ref="newUserForm" @submit.prevent="createNewUser">
          <v-text-field
            v-model="newUser.email"
            type="email"
            label="Email"
            required
            :rules="[
              (v) => !!v || 'Email address is required',
              (v) => /.+@.+\..+/.test(v) || 'Email must be valid',
            ]"
          />
          <v-text-field
            v-model="newUser.full_name"
            label="Full Name"
            required
            :rules="[(v) => !!v || 'Full name is required']"
          />
          <v-select
            v-model="newUser.role"
            :items="roles"
            label="Role"
            :rules="[(v) => !!v || 'User role is required']"
            required
          />

          <v-btn type="submit" color="primary">Create User</v-btn>
        </v-form>

        <v-alert v-if="adminSuccessMessage" type="info" class="mt-4">
          <span>{{ adminSuccessMessage }}<br />Generated Password: {{ generatedPassword }}</span>
          <v-icon class="ml-2 cursor-pointer" size="18" @click="copyPassword">
            mdi-content-copy
          </v-icon>
          <span v-if="passwordCopied" class="ml-2"><br />Password Copied Successfully!</span>
        </v-alert>
        <v-alert v-if="adminErrorMessage" type="error" class="mt-4">{{adminErrorMessage}}</v-alert>
      </v-card>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import userService from '@/services/userService'
import { useAuthStore } from '@/stores/authStore'
import utils from '@/utils/utils'

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const passwordForm = ref(null)
const newUserForm = ref(null)
const generatedPassword = ref('')
const passwordCopied = ref(false)
const adminSuccessMessage = ref('')
const adminErrorMessage = ref('')
const roles = ['Admin', 'Researcher', 'Technician'] // Example roles for user creation
const newUser = ref({
  email: '',
  full_name: '',
  role: '',
})

const authStore = useAuthStore()
// Handle form submission for personal password change
const submitPasswordForm = () => {
  // Validate the password change form
  if (currentPassword.value && newPassword.value && newPassword.value === confirmPassword.value) {
    // Update Password
    userService
      .patchUserPassword(authStore.getUser.uuid, currentPassword.value, newPassword.value)
      .then((response) => {
        authStore.setToken(response.access_token)
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
// Handle new user creation
const createNewUser = () => {
  // Validate Form
  newUserForm.value?.validate().then((isValid) => {
    if (!isValid.valid) return

    // Generate a random password for the new user
    generatedPassword.value = utils.generateRandomPassword();
    const user = {
      email: newUser.value.email,
      full_name: newUser.value.full_name,
      role: newUser.value.role,
      password: generatedPassword.value,
    };

    userService.postUser(user)
      .then(() => {
        adminSuccessMessage.value = 'New user created successfully.'
        adminErrorMessage.value = ''
      })
      .catch((error) => {
        adminErrorMessage.value = 'Failed to create new user: ' + error.detail
        adminSuccessMessage.value = ''
      })

    newUserForm.value.reset();
    newUserForm.value.resetValidation();
    newUser.value = { email: '', full_name: '', role: '' };
  });
};

// Copy the password to the clipboard
const copyPassword = () => {
  navigator.clipboard.writeText(generatedPassword.value).then(() => {
    passwordCopied.value = true
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
