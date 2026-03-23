<template>
  <v-app-bar app color="transparent" elevation="0" class="app-bar-frame">
    <div class="app-nav-shell d-flex align-center w-100">
      <v-toolbar-title class="app-nav-logo">
        <router-link to="/home">
          <LogoRentElektroSVG fillColor="white" />
        </router-link>
      </v-toolbar-title>
      <v-spacer />
      <div class="d-none d-md-flex align-center ga-2 app-nav-links">
        <AppButton variant="text" to="/home">Strona glowna</AppButton>
        <AppButton variant="text" to="/about">O serwisie</AppButton>
        <AppButton variant="text" to="/tools">Narzedzia</AppButton>
        <AppButton v-if="!isAuthenticated" variant="text" to="/login">Logowanie</AppButton>
        <AppButton v-if="!isAuthenticated" color="secondary" to="/signup">Rejestracja</AppButton>
        <AppButton v-if="isAuthenticated" variant="text" to="/profile">Profil</AppButton>
        <AppButton v-if="isAuthenticated" color="secondary" @click="logout">Wyloguj</AppButton>
      </div>
    </div>
  </v-app-bar>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';
import LogoRentElektroSVG from '@/shared/branding/LogoRentElektroSVG.vue';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import eventBus from '@/eventBus';

const router = useRouter();
const { isAuthenticated, syncSessionState, logout: performLogout } = useAuth();

const handleLogin = (): void => {
  void syncSessionState();
};

const handleLogout = (): void => {
  void syncSessionState();
};

const logout = async (): Promise<void> => {
  await performLogout();
  eventBus.emit('logout');
  await router.push('/login');
};

onMounted(() => {
  eventBus.on('login', handleLogin);
  eventBus.on('logout', handleLogout);
  void syncSessionState();
});

onBeforeUnmount(() => {
  eventBus.off('login', handleLogin);
  eventBus.off('logout', handleLogout);
});
</script>
