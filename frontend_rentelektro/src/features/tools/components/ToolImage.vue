<template>
  <v-img
    :src="imageUrl"
    height="420"
    cover
    class="rounded-lg"
    :aspect-ratio="4 / 3"
  >
    <template #placeholder>
      <div class="d-flex align-center justify-center fill-height bg-grey-lighten-3">
        <v-icon size="56" color="grey-darken-1">mdi-tools</v-icon>
      </div>
    </template>
  </v-img>
</template>

<script setup lang="ts">
defineProps<{
  imageUrl: string;
}>();
</script>
