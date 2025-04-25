<template>
  <div style="height: 100vh; overflow: hidden;">
    <v-container class="fill-height pa-0">
      <v-row class="d-flex align-stretch fill-height" align="stretch" no-gutters>
        <v-col cols="6" class="d-flex">
          <v-card class="pa-4" elevation="2" style="width: 100%; height: 100%">
            <v-card-title class="text-h6">Projects</v-card-title>
            <v-card-text>
              <p>Total: 12</p>
              <p>Active: 5</p>
              <p>Recently Updated: 3</p>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" class="d-flex">
          <v-card class="pa-4" elevation="2" style="width: 100%; height: 100%">
            <v-card-title class="text-h6">Commercial Sensors</v-card-title>
            <v-card-text>
              <p>Total: 24</p>
              <p>Vendors: 8</p>
              <p>Pending Reviews: 2</p>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" class="d-flex">
          <v-card class="pa-4" elevation="2" style="width: 100%; height: 100%">
            <v-card-title class="text-h6">Sensor Nodes</v-card-title>
            <v-card-text>
              <p>Total: 40</p>
              <p>Online: 36</p>
              <p>Offline: 4</p>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" class="d-flex">
          <v-card class="pa-4" elevation="2" style="width: 100%; height: 100%">
            <v-card-title class="text-h6">Sensor Templates</v-card-title>
            <v-card-text>
              <p>Total: 15</p>
              <p>Used in Projects: 9</p>
              <p>Unused: 6</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>