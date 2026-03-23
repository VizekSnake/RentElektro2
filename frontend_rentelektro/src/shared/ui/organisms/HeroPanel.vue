<template>
  <div :class="panelClass">
    <div>
      <div v-if="eyebrow" class="text-overline text-medium-emphasis">{{ eyebrow }}</div>
      <h2 :class="titleClass">{{ title }}</h2>
      <p v-if="subtitle" :class="subtitleClass">
        {{ subtitle }}
      </p>
      <div v-if="$slots.default" :class="contentClass">
        <slot />
      </div>
    </div>

    <div v-if="$slots.tags || $slots.actions" :class="sideClass">
      <slot name="tags" />
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title: string;
  subtitle?: string;
  eyebrow?: string;
  panelClass?: string;
  titleClass?: string;
  subtitleClass?: string;
  contentClass?: string;
  sideClass?: string;
}>(), {
  subtitle: '',
  eyebrow: '',
  panelClass: 'app-tool-hero',
  titleClass: 'text-h3 font-weight-black',
  subtitleClass: 'text-body-1 text-medium-emphasis mt-2 mb-0',
  contentClass: 'mt-4',
  sideClass: 'd-flex flex-wrap ga-3',
});
</script>
