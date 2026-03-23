<template>
  <v-btn
    :color="color"
    :variant="variant"
    :size="size"
    :block="block"
    :loading="loading"
    :disabled="disabled"
    :prepend-icon="prependIcon"
    :append-icon="appendIcon"
    v-bind="$attrs"
  >
    <slot />
  </v-btn>
</template>

<script setup lang="ts">
defineOptions({
  inheritAttrs: false,
});

withDefaults(defineProps<{
  color?: string;
  variant?: 'flat' | 'text' | 'outlined' | 'tonal' | 'plain' | 'elevated';
  size?: 'x-small' | 'small' | 'default' | 'large' | 'x-large';
  block?: boolean;
  loading?: boolean;
  disabled?: boolean;
  prependIcon?: string;
  appendIcon?: string;
}>(), {
  color: 'primary',
  variant: 'flat',
  size: 'default',
  block: false,
  loading: false,
  disabled: false,
  prependIcon: undefined,
  appendIcon: undefined,
});
</script>
