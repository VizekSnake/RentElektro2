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
    <v-btn class="ma-2" text to="/tools">Narzędzia</v-btn>
    <v-btn v-if="!isAuthenticated" class="ma-2" text to="/login">Logowanie</v-btn>
    <v-btn v-if="!isAuthenticated" class="ma-2" text to="/signup">Rejestracja</v-btn>
    <v-btn v-if="isAuthenticated" class="ma-2" text to="/profile">Profil</v-btn>
    <v-btn v-if="isAuthenticated" class="ma-2" text @click="logout">Wyloguj</v-btn>
  </v-app-bar>
</template>

<script>
import LogoRentElektroSVG from './LogoRentElektroSVG.vue';
import eventBus from '@/eventBus';
import {isTokenExpired, removeToken} from '@/services/authService';

export default {
  name: 'BaseNavbar',
  components: {
    LogoRentElektroSVG
  },
  data() {
    return {
      isAuthenticated: !!localStorage.getItem('access_token')
    };
  },
  created() {
    eventBus.on('login', () => {
      this.isAuthenticated = true;
    });
    eventBus.on('logout', () => {
      this.isAuthenticated = false;
    });

    // Check token expiration periodically
    this.tokenCheckInterval = setInterval(() => {
      if (isTokenExpired()) {
        this.logout();
      }
    }, 1000 * 60); // Check every minute
  },
  beforeUnmount() {
    // Clear the interval when the component is destroyed
    clearInterval(this.tokenCheckInterval);
  },
  methods: {
    logout() {
      removeToken();
      this.isAuthenticated = false;
      eventBus.emit('logout');
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
</style>