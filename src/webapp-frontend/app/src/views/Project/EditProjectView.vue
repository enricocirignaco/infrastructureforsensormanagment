<template>
    <ProjectForm :project-id="route.params.id" />
</template>

<script setup>
import { useRoute } from 'vue-router'
import ProjectForm from '@/components/ProjectForm.vue'
const route = useRoute()
</script>