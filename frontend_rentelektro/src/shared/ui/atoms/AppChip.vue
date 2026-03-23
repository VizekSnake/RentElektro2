<template>
  <v-chip
    :color="color"
    :variant="variant"
    :size="size"
    v-bind="$attrs"
  >
    <slot />
  </v-chip>
</template>

<script setup lang="ts">
defineOptions({
  inheritAttrs: false,
});

withDefaults(defineProps<{
  color?: string;
  variant?: 'flat' | 'text' | 'outlined' | 'tonal' | 'plain' | 'elevated';
  size?: 'x-small' | 'small' | 'default' | 'large' | 'x-large';
}>(), {
  color: 'primary',
  variant: 'tonal',
  size: 'default',
});
</script>
