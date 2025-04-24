<template>
    <CommercialSensorForm :sensor-id="route.params.id" />
</template>

<script setup>
import { useRoute } from 'vue-router'
import CommercialSensorForm from '@/components/CommercialSensorForm.vue'
const route = useRoute()
</script>