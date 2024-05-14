<!-- src/views/BaseHome.vue -->
<template>
  <div>
    <BaseNavbar />
    <main>
      <h1>Welcome to MyApp!</h1>
      <p>This is the homepage of your Vue application.</p>
    </main>
  </div>
</template>

<script>
// Import the Navbar component
import BaseNavbar from '@/components/BaseNavbar.vue'

export default {
  name: 'BaseHome',
  components: {
    BaseNavbar
  }
}
</script>

<style scoped>
main {
  padding: 20px;
  text-align: center;
}
</style>
