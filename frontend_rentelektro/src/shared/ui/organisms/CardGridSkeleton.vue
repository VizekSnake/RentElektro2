<template>
  <v-row>
    <v-col v-for="item in items" :key="item" cols="12" md="6" lg="4">
      <SkeletonCard :type="type" />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import SkeletonCard from '@/shared/ui/molecules/SkeletonCard.vue';

withDefaults(defineProps<{
  items?: number;
  type?: string;
}>(), {
  items: 6,
  type: 'image, article, actions',
});
</script>
