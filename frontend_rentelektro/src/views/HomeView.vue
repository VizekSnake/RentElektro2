<template>
  <v-container class="app-home">
    <section class="app-home-hero">
      <div class="app-home-hero-grid">
        <div class="d-flex flex-column ga-6">
          <div class="app-home-kicker">
            <v-icon size="18">mdi-star-four-points</v-icon>
            RentElektro Marketplace
          </div>

          <div class="d-flex flex-column ga-4">
            <h1 class="app-home-title text-high-emphasis font-weight-black ma-0">
              Wynajem narzędzi w premium wydaniu.
            </h1>
            <p class="app-home-copy ma-0">
              Jasny, szybki katalog dla osób, które chcą wystawić ofertę albo zarezerwować sprzęt bez ciężkiego panelu i przypadkowego chaosu. Pomarańczowy prowadzi interakcję, reszta zostaje czysta i spokojna.
            </p>
          </div>

          <div class="d-flex flex-wrap ga-3">
            <AppButton to="/tools" size="large" prepend-icon="mdi-arrow-top-right-thin-circle-outline">
              Przeglądaj narzędzia
            </AppButton>
            <AppButton to="/tool/add" size="large" variant="outlined" color="secondary" prepend-icon="mdi-plus-circle-outline">
              Dodaj ofertę
            </AppButton>
          </div>

          <div class="app-home-stat-grid">
            <div class="app-home-glass-card">
              <div class="app-home-stat-value">24h</div>
              <div class="app-home-stat-label">na szybkie wystawienie i obsługę zapytań</div>
            </div>
            <div class="app-home-glass-card">
              <div class="app-home-stat-value">Jeden</div>
              <div class="app-home-stat-label">czytelny katalog zamiast rozproszonych ogłoszeń</div>
            </div>
            <div class="app-home-glass-card">
              <div class="app-home-stat-value">Zero</div>
              <div class="app-home-stat-label">panelowego bałaganu w głównej ścieżce użytkownika</div>
            </div>
          </div>
        </div>

        <div class="app-home-showcase">
          <div v-if="showcaseTools.length" class="app-home-showcase-grid">
            <article
              v-for="(item, index) in showcaseTools"
              :key="item.id"
              class="app-home-showcase-tile"
              :class="{ 'is-featured': index === 0 }"
            >
              <v-img
                :src="item.ImageURL"
                :alt="`${item.Brand} ${item.Type}`"
                cover
                class="app-home-showcase-image"
              />
            </article>
          </div>
          <div v-else class="app-home-showcase-empty">
            Najnowsze oferty pojawią się tutaj, gdy w katalogu będą dostępne zdjęcia narzędzi.
          </div>
        </div>
      </div>
    </section>

    <section class="app-home-section">
      <v-row>
        <v-col cols="12" md="4">
          <div class="app-home-feature-card">
            <div class="app-home-feature-icon mb-4">
              <v-icon size="26">mdi-view-dashboard-outline</v-icon>
            </div>
            <h3 class="text-h6 font-weight-bold mb-2">Minimalny onboarding</h3>
            <p class="app-muted-copy mb-0">
              Wejście do katalogu, logowanie i dodawanie ofert są podane wprost, bez zbędnych warstw i bocznych paneli.
            </p>
          </div>
        </v-col>
        <v-col cols="12" md="4">
          <div class="app-home-feature-card">
            <div class="app-home-feature-icon mb-4">
              <v-icon size="26">mdi-image-filter-hdr</v-icon>
            </div>
            <h3 class="text-h6 font-weight-bold mb-2">Lżejsza estetyka</h3>
            <p class="app-muted-copy mb-0">
              Jasne powierzchnie, duża typografia i akcent pomarańczowy budują bardziej nowoczesny, produktowy charakter.
            </p>
          </div>
        </v-col>
        <v-col cols="12" md="4">
          <div class="app-home-feature-card">
            <div class="app-home-feature-icon mb-4">
              <v-icon size="26">mdi-lightning-bolt-outline</v-icon>
            </div>
            <h3 class="text-h6 font-weight-bold mb-2">Szybka decyzja</h3>
            <p class="app-muted-copy mb-0">
              Użytkownik od razu widzi, gdzie przejść do narzędzi, gdzie dodać ofertę i jaki jest główny przebieg rezerwacji.
            </p>
          </div>
        </v-col>
      </v-row>
    </section>

    <section class="app-home-cta">
      <v-row align="center">
        <v-col cols="12" md="8">
          <div class="text-overline text-white text-opacity-80">Start</div>
          <div class="text-h4 font-weight-bold mb-2">Możesz od razu przejść do katalogu albo wystawić pierwsze narzędzie.</div>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-md-end">
          <div class="d-flex flex-wrap ga-3">
            <AppButton to="/tools" color="secondary" size="large">Katalog</AppButton>
            <AppButton to="/signup" variant="outlined" color="white" size="large">Dołącz teraz</AppButton>
          </div>
        </v-col>
      </v-row>
    </section>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { fetchTools } from '@/services/toolService';
import AppButton from '@/shared/ui/atoms/AppButton.vue';

import type { Tool } from '@/types/tools';

const latestTools = ref<Tool[]>([]);

const showcaseTools = computed(() =>
  latestTools.value
    .filter((item) => Boolean(item.ImageURL))
    .slice(0, 5),
);

onMounted(async () => {
  try {
    const response = await fetchTools({ sort: 'newest', page: 1, page_size: 6 });
    latestTools.value = response.items;
  } catch {
    latestTools.value = [];
  }
});
</script>
