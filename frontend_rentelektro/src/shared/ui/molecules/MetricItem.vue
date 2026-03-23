<template>
  <div>
    <div class="text-caption text-medium-emphasis">{{ label }}</div>
    <div :class="valueClass">{{ value }}</div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  label: string;
  value: string | number;
  valueClass?: string;
}>(), {
  valueClass: 'text-body-1 font-weight-medium',
});
</script>
