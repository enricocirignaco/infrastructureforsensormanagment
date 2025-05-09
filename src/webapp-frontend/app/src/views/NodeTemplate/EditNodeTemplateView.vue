<template>
    <NodeTemplateForm :node-template-id="route.params.id" />
</template>

<script setup>
import { useRoute } from 'vue-router'
import NodeTemplateForm from '@/components/NodeTemplateForm.vue'
const route = useRoute()
</script>