<template>
  <v-container>
    <MainBanner
      imageUrl=""
      title="About Us"
      subtitle="Learn more about our journey"
    />
    <!-- Reszta zawartości widoku -->
  </v-container>
</template>

<script>
import MainBanner from '@/components/MainBanner.vue';

export default {
  name: 'AboutView',
  components: {
   MainBanner
  }
};
</script>

<style scoped>
</style>