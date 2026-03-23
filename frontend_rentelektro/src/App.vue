<template>
  <v-app>
    <BaseNavbar />
    <v-main class="app-main">
      <router-view/>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import BaseNavbar from "@/shared/navigation/organisms/BaseNavbar.vue";
</script>
