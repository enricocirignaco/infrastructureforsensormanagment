<template>
  <v-app>
    <!-- Sidebar (Rail Variant) -->
    <v-navigation-drawer :rail="rail" permanent color="primary">
      <v-list-item
        nav
        style="cursor: pointer"
        @click="rail = !rail"
        :title="authStore.getUser?.full_name || ''"
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
          :prepend-icon="textStore.icons.projects"
          title="Projects"
          value="projects"
          @click="router.push('/projects')"
        ></v-list-item>
        <v-list-item
          :prepend-icon="textStore.icons.sensorNodes"
          title="Sensor Nodes"
          value="sensorNodes"
          @click="router.push('/sensor-nodes')"
        ></v-list-item>
        <v-list-item
          :prepend-icon="textStore.icons.nodeTemplates"
          title="Node Templates"
          value="nodeTemplates"
          @click="router.push('/node-templates')"
        ></v-list-item>
        <v-list-item
          :prepend-icon="textStore.icons.commercialSensors"
          title="Commercial Sensors"
          value="sensors"
          @click="router.push('/commercial-sensors')"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Header (Navbar) -->
    <v-app-bar app color="primary">
      <v-toolbar-title style="cursor: pointer" @click="router.push('/')">
        {{ textStore.applicationName }}
      </v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Version Banner -->
      <v-chip
        class="mx-1"
        size="x-small"
        variant="outlined"
        color="secondary"
        style="opacity: 0.7;"
      >
        {{ textStore?.appVersion}}
      </v-chip>

      <!-- Custom Dark Mode Toggle -->
      <DarkModeToggle class="mx-1" />

      <!-- Settings Button -->
      <v-btn icon color="secondary" class="mx-1" @click="router.push('/settings')">
        <v-icon>mdi-cog-outline</v-icon>
      </v-btn>

      <!-- Logout Button -->
      <v-btn icon color="secondary" class="mx-1" @click="logout">
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
  authStore.clearToken()
  router.push('/login')
}
</script>
