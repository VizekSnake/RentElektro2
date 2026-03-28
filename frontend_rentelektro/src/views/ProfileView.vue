<template>
  <v-container class="app-profile-page">
    <section class="app-profile-page-hero">
      <div class="app-home-kicker">
        <v-icon size="18">mdi-account-circle-outline</v-icon>
        Twoje konto
      </div>
      <h1 class="app-product-title ma-0 mt-4">Profil użytkownika</h1>
      <p class="app-product-copy mt-3 mb-0">
        Zarządzaj danymi konta, zdjęciem, ustawieniami i podstawową tożsamością w tym samym nowoczesnym stylu co reszta produktu.
      </p>
    </section>

    <MainProfile />
  </v-container>
</template>

<script setup lang="ts">
import MainProfile from '@/features/profile/components/MainProfile.vue';
</script>
