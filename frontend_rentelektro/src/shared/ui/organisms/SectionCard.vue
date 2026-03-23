<template>
  <v-card
    class="rounded-xl app-section-card"
    :variant="variant"
    :elevation="elevation"
    :border="border"
  >
    <v-card-item v-if="title || subtitle">
      <v-card-title v-if="title" class="app-section-title">{{ title }}</v-card-title>
      <v-card-subtitle v-if="subtitle" class="app-section-subtitle">{{ subtitle }}</v-card-subtitle>
    </v-card-item>
    <v-card-text class="pa-4 pa-md-6">
      <slot />
    </v-card-text>
    <v-card-actions v-if="$slots.actions" class="px-4 px-md-6 pb-4">
      <slot name="actions" />
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title?: string;
  subtitle?: string;
  variant?: string;
  elevation?: number | string;
  border?: boolean | string;
}>(), {
  title: '',
  subtitle: '',
  variant: 'flat',
  elevation: 2,
  border: 'sm',
});
</script>
