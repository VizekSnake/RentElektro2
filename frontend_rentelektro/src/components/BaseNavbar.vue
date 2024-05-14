<!-- src/components/BaseNavbar.vue -->
<template>
  <nav class="navbar">
    <div class="logo">
      <a href="/">RentElektro 2</a>
    </div>
    <div class="nav-links">
      <router-link to="/home">Home</router-link>
      <router-link to="/about">About</router-link>
      <router-link to="/login">Login</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'BaseNavbar'
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 50px;
  background-color: darkorange;
  color: white;
}

.logo a {
  color: white;
  text-decoration: none;
  font-size: 20px;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 20px; /* Dodaje odstępy pomiędzy linkami */
}

.nav-links a {
  color: white;
  text-decoration: none;
}
</style>
