<template>
    <SensorNodeForm :sensor-node-id="route.params.id" />
</template>

<script setup>
import { useRoute } from 'vue-router'
import SensorNodeForm from '@/components/SensorNodeForm.vue';
const route = useRoute()
</script>