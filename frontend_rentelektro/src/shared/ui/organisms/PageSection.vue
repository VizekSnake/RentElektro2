<template>
  <v-container class="py-6 py-md-8">
    <SectionHeader
      :title="title"
      :subtitle="subtitle"
      wrapper-class="mb-6"
    >
      <template #actions>
        <slot name="actions" />
      </template>
    </SectionHeader>

    <slot />
  </v-container>
</template>

<script setup lang="ts">
import SectionHeader from '@/shared/ui/molecules/SectionHeader.vue';

defineProps<{
  title: string;
  subtitle?: string;
}>();
</script>
