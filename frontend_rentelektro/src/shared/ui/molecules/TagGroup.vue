<template>
  <div class="d-flex align-center flex-wrap ga-2">
    <AppChip
      v-for="tag in tags"
      :key="tag.label"
      :color="tag.color"
      :variant="tag.variant"
      :size="tag.size"
    >
      {{ tag.label }}
    </AppChip>
  </div>
</template>

<script setup lang="ts">
import AppChip from '@/shared/ui/atoms/AppChip.vue';

export type TagGroupItem = {
  label: string;
  color?: string;
  variant?: 'flat' | 'text' | 'outlined' | 'tonal' | 'plain' | 'elevated';
  size?: 'x-small' | 'small' | 'default' | 'large' | 'x-large';
};

defineProps<{
  tags: TagGroupItem[];
}>();
</script>
