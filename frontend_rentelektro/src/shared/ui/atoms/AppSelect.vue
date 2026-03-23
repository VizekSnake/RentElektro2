<template>
  <v-select
    :model-value="modelValue"
    :label="label"
    :items="items"
    :item-title="itemTitle"
    :item-value="itemValue"
    :rules="rules"
    :hint="hint"
    :persistent-hint="persistentHint"
    :prepend-inner-icon="prependInnerIcon"
    :disabled="disabled"
    :loading="loading"
    v-bind="$attrs"
    @update:model-value="emit('update:modelValue', $event)"
  />
</template>

<script setup lang="ts" generic="TItem">
defineOptions({
  inheritAttrs: false,
});

defineProps<{
  modelValue?: string | number | boolean | null;
  label?: string;
  items?: TItem[];
  itemTitle?: string;
  itemValue?: string;
  rules?: unknown[];
  hint?: string;
  persistentHint?: boolean;
  prependInnerIcon?: string;
  disabled?: boolean;
  loading?: boolean;
}>();

const emit = defineEmits<{
  'update:modelValue': [value: string | number | boolean | null];
}>();
</script>
