<template>
  <v-select
    :model-value="modelValue"
    :label="label"
    :items="items"
    :item-title="itemTitle"
    :item-value="itemValue"
    :rules="normalizedRules"
    :hint="hint"
    :persistent-hint="persistentHint"
    :prepend-inner-icon="prependInnerIcon"
    :disabled="disabled"
    :loading="loading"
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
  modelValue?: string | number | boolean | symbol | null;
  label?: string;
  items?: readonly unknown[];
  itemTitle?: string;
  itemValue?: string;
  rules?: unknown[];
  hint?: string;
  persistentHint?: boolean;
  prependInnerIcon?: string;
  disabled?: boolean;
  loading?: boolean;
}>();

const normalizedRules = computed(() => props.rules as never);

const emit = defineEmits<{
  'update:modelValue': [value: string | number | boolean | symbol | null];
}>();
</script>
