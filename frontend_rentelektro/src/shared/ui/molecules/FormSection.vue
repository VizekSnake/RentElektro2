<template>
  <div class="d-flex flex-column ga-4">
    <div>
      <h3 class="text-h6 font-weight-bold">{{ title }}</h3>
      <p v-if="description" class="text-body-2 text-medium-emphasis">
        {{ description }}
      </p>
    </div>

    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  description?: string;
}>();
</script>
