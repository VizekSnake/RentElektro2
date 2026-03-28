<template>
  <v-textarea
    :model-value="modelValue"
    :label="label"
    :rules="normalizedRules"
    :hint="hint"
    :persistent-hint="persistentHint"
    :prepend-inner-icon="prependInnerIcon"
    :rows="rows"
    :auto-grow="autoGrow"
    :placeholder="placeholder"
    :disabled="disabled"
    v-bind="$attrs"
    @update:model-value="emit('update:modelValue', $event)"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';

defineOptions({
  inheritAttrs: false,
});

const props = defineProps<{
  modelValue?: string | null;
  label?: string;
  rules?: unknown[];
  hint?: string;
  persistentHint?: boolean;
  prependInnerIcon?: string;
  rows?: string | number;
  autoGrow?: boolean;
  placeholder?: string;
  disabled?: boolean;
}>();

const normalizedRules = computed(() => props.rules as never);

const emit = defineEmits<{
  'update:modelValue': [value: string | null];
}>();
</script>
