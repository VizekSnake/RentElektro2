<template>
  <v-checkbox
    :model-value="modelValue"
    :label="label"
    :hide-details="hideDetails"
    :disabled="disabled"
    v-bind="$attrs"
    @update:model-value="emit('update:modelValue', $event)"
  />
</template>

<script setup lang="ts">
defineOptions({
  inheritAttrs: false,
});

withDefaults(defineProps<{
  modelValue?: boolean | null;
  label?: string;
  hideDetails?: boolean;
  disabled?: boolean;
}>(), {
  modelValue: false,
  label: '',
  hideDetails: false,
  disabled: false,
});

const emit = defineEmits<{
  'update:modelValue': [value: boolean | null];
}>();
</script>
