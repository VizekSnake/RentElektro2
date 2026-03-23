<template>
  <div class="pa-4 rounded-xl app-stat-card">
    <div class="text-caption text-white text-opacity-70">{{ label }}</div>
    <div class="text-h5 font-weight-bold">{{ value }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string;
  value: string;
}>();
</script>
