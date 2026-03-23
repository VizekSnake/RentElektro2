<template>
  <v-skeleton-loader :type="type" class="rounded-xl app-skeleton-card" />
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  type?: string;
}>(), {
  type: 'article',
});
</script>
