<template>
  <v-text-field
    :model-value="modelValue"
    :label="label"
    :type="type"
    :rules="normalizedRules"
    :hint="hint"
    :persistent-hint="persistentHint"
    :prepend-inner-icon="prependInnerIcon"
    :append-inner-icon="appendInnerIcon"
    :autocomplete="autocomplete"
    :required="required"
    :disabled="disabled"
    :loading="loading"
    v-bind="$attrs"
    @update:model-value="emit('update:modelValue', $event)"
    @click:append-inner="emit('click:appendInner', $event)"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';

defineOptions({
  inheritAttrs: false,
});

const props = defineProps<{
  modelValue?: string | number | null;
  label?: string;
  type?: string;
  rules?: unknown[];
  hint?: string;
  persistentHint?: boolean;
  prependInnerIcon?: string;
  appendInnerIcon?: string;
  autocomplete?: string;
  required?: boolean;
  disabled?: boolean;
  loading?: boolean;
}>();

const normalizedRules = computed(() => props.rules as never);

const emit = defineEmits<{
  'update:modelValue': [value: string | number | null];
  'click:appendInner': [event: MouseEvent];
}>();
</script>
