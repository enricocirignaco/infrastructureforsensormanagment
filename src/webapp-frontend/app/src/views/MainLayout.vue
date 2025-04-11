<template>
  <v-app>
    <!-- Sidebar (Rail Variant) -->
    <v-navigation-drawer :rail="rail" permanent color="primary">
      <v-list-item
        nav
        style="cursor: pointer"
        @click="rail = !rail"
        :title="authStore.getUser.full_name"
      >
        <template #prepend>
          <v-avatar size="48">
            <v-img src="/images/logo.svg" />
          </v-avatar>
        </template>
      </v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-forest-outline"
          title="Projects"
          value="projects"
          @click="router.push('/projects')"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-passport-biometric"
          title="Sensor Nodes"
          value="sensorNodes"
          @click="router.push('/sensor-nodes')"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-plus-box-multiple"
          title="Node Templates"
          value="nodeTemplates"
          @click="router.push('/node-templates')"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-test-tube-empty"
          title="Sensors"
          value="sensors"
          @click="router.push('/snesors')"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Header (Navbar) -->
    <v-app-bar app color="primary">
      <v-toolbar-title style="cursor: pointer" @click="router.push('/')">{{
        textStore.applicationName
      }}</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Custom Dark Mode Toggle -->
      <DarkModeToggle />

      <!-- Settings Button -->
      <v-btn icon color="secondary" @click="router.push('/settings')">
        <v-icon>mdi-cog-outline</v-icon>
      </v-btn>

      <!-- Logout Button -->
      <v-btn icon color="secondary" @click="logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Main content -->
    <v-main>
      <v-container>
        <router-view />
        <!-- This will render the child views -->
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app color="secondary">
      <v-col class="text-center" cols="12">
        <h3>{{ textStore.slogan }}</h3>
        <span>&copy; {{ textStore.applicationName }}</span>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import router from '@/router'
import { useTextStore } from '@/stores/textStore'
import { useAuthStore } from '@/stores/authStore'
import DarkModeToggle from '@/components/ThemeToggle.vue'

const textStore = useTextStore()
const rail = ref(true)
const authStore = useAuthStore()

// Logout Functionality
const logout = () => {
  // Remove user session and redirect to login page
  console.log(authStore.getUser)
  authStore.clearToken()
  router.push('/login')
}
</script>
