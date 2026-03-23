<template>
  <div class="d-flex flex-column flex-md-row align-start align-md-center justify-space-between ga-4" :class="wrapperClass">
    <div>
      <h1 :class="titleClass">
        {{ title }}
      </h1>
      <p
        v-if="subtitle"
        :class="subtitleClass"
      >
        {{ subtitle }}
      </p>
    </div>
    <slot name="actions" />
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title: string;
  subtitle?: string;
  wrapperClass?: string;
  titleClass?: string;
  subtitleClass?: string;
}>(), {
  subtitle: '',
  wrapperClass: '',
  titleClass: 'text-h4 font-weight-bold text-high-emphasis',
  subtitleClass: 'text-body-1 text-medium-emphasis mt-2',
});
</script>
