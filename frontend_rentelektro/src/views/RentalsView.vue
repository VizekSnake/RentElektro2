<template>
  <v-container class="app-profile-page">
    <section class="app-profile-page-hero">
      <div class="app-home-kicker">
        <v-icon size="18">mdi-bell-badge-outline</v-icon>
        Centrum wynajmów
      </div>
      <h1 class="app-product-title ma-0 mt-4">Zarządzaj swoimi wynajmami</h1>
      <p class="app-product-copy mt-3 mb-0">
        Sprawdzaj nowe zgłoszenia do akceptacji, własne prośby o wynajem oraz historię zakończonych spraw bez mieszania tego z ustawieniami konta.
      </p>
    </section>

    <RentalInboxPanel />
  </v-container>
</template>

<script setup lang="ts">
import RentalInboxPanel from '@/features/profile/components/RentalInboxPanel.vue';
</script>
