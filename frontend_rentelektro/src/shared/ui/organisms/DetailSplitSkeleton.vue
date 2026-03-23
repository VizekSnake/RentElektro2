<template>
  <v-row>
    <v-col cols="12" md="6">
      <SkeletonCard type="image" />
    </v-col>
    <v-col cols="12" md="6">
      <SkeletonCard type="article, article" />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import SkeletonCard from '@/shared/ui/molecules/SkeletonCard.vue';
</script>
