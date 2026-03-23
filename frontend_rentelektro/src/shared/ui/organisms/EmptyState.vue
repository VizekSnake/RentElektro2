<template>
  <SectionCard :title="title" :subtitle="subtitle">
    <template v-if="$slots.default">
      <slot />
    </template>
    <template v-if="$slots.actions" #actions>
      <slot name="actions" />
    </template>
  </SectionCard>
</template>

<script setup lang="ts">
import SectionCard from '@/shared/ui/organisms/SectionCard.vue';

defineProps<{
  title: string;
  subtitle: string;
}>();
</script>
