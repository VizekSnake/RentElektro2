<template>
  <v-app-bar app color="orange">
    <v-toolbar-title>
      <router-link to="/home">
        <LogoRentElektroSVG fillColor="white" />
      </router-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn class="ma-2" text to="/home">Strona główna</v-btn>
    <v-btn class="ma-2" text to="/about">O serwisie</v-btn>
    <v-btn v-if="!isAuthenticated" class="ma-2" text to="/login">Logowanie</v-btn>
    <v-btn v-if="!isAuthenticated" class="ma-2" text to="/signup">Rejestracja</v-btn>
    <v-btn v-if="isAuthenticated" class="ma-2" text to="/profile">Profil</v-btn>
    <v-btn v-if="isAuthenticated" class="ma-2" text @click="logout">Wyloguj</v-btn>
  </v-app-bar>
</template>

<script>
import LogoRentElektroSVG from './LogoRentElektroSVG.vue';

export default {
  name: 'BaseNavbar',
  components: {
    LogoRentElektroSVG
  },
  data() {
    return {
      isAuthenticated: false
    };
  },
  created() {
    // Replace this with actual logic to check if the user is authenticated
    this.isAuthenticated = !!localStorage.getItem('access_token');
  },
  methods: {
    logout() {
      // Replace this with actual logout logic
      localStorage.removeItem('access_token');
      this.isAuthenticated = false;
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
</style>
