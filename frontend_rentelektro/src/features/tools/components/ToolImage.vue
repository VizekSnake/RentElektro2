<template>
  <div class="app-tool-detail-image-shell">
    <v-img
      :src="imageUrl"
      height="420"
      contain
      class="app-tool-detail-image"
      :aspect-ratio="4 / 3"
    >
      <template #placeholder>
        <div class="app-tool-detail-image-placeholder">
          <v-icon size="56" color="grey-darken-1">mdi-tools</v-icon>
        </div>
      </template>
    </v-img>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  imageUrl: string;
}>();
</script>
