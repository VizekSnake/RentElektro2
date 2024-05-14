<template>
  <v-app>
    <BaseNavbar />
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script setup>
import BaseNavbar from "@/components/BaseNavbar.vue";
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
