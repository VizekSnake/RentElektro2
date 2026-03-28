<template>
  <v-app>
    <BaseNavbar />
    <v-main class="app-main">
      <router-view/>
    </v-main>
    <BaseFooter />
  </v-app>
</template>

<script setup lang="ts">
import BaseNavbar from "@/shared/navigation/organisms/BaseNavbar.vue";
import BaseFooter from "@/shared/navigation/organisms/BaseFooter.vue";
</script>
