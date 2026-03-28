<template>
  <div class="app-tool-add-page">
    <v-container class="app-max-width">
      <section class="app-tool-add-hero">
        <div class="app-tool-add-hero-grid">
          <div class="d-flex flex-column ga-6">
            <div class="d-flex flex-column ga-4">
              <div class="app-home-kicker">
                <v-icon size="18">mdi-plus-circle-outline</v-icon>
                Dodaj ofertę
              </div>
              <h1 class="app-product-title ma-0">Pokaż sprzęt tak, żeby ktoś chciał go od razu wynająć.</h1>
              <p class="app-product-copy mb-0">
                Dobra oferta to jasna nazwa, konkretne zdjęcie, uczciwa stawka i krótki opis stanu.
                Wypełnij formularz raz, a Twoje narzędzie od razu trafi do katalogu.
              </p>
            </div>

            <div class="app-tool-add-stat-grid">
              <div class="app-product-stat-card">
                <span class="app-product-stat-label">Najważniejsze</span>
                <strong class="app-product-stat-value">Zdjęcie + cena</strong>
              </div>
              <div class="app-product-stat-card">
                <span class="app-product-stat-label">Dla najemcy</span>
                <strong class="app-product-stat-value">Czytelny opis</strong>
              </div>
              <div class="app-product-stat-card">
                <span class="app-product-stat-label">Po publikacji</span>
                <strong class="app-product-stat-value">Widoczne w katalogu</strong>
              </div>
            </div>
          </div>

          <div class="app-tool-add-side-shell">
            <div class="app-tool-add-side-card">
              <div class="text-overline mb-2">Szybka checklista</div>
              <div class="d-flex flex-column ga-3">
                <div class="app-tool-add-check">
                  <v-icon size="18" color="primary">mdi-check-circle-outline</v-icon>
                  <span>Użyj konkretnej nazwy, np. „Wiertarka udarowa”.</span>
                </div>
                <div class="app-tool-add-check">
                  <v-icon size="18" color="primary">mdi-check-circle-outline</v-icon>
                  <span>Dodaj zdjęcie, które dobrze pokazuje realny stan sprzętu.</span>
                </div>
                <div class="app-tool-add-check">
                  <v-icon size="18" color="primary">mdi-check-circle-outline</v-icon>
                  <span>Podaj stawkę za dzień, żeby oferta była od razu porównywalna.</span>
                </div>
                <div class="app-tool-add-check">
                  <v-icon size="18" color="primary">mdi-check-circle-outline</v-icon>
                  <span>Napisz, do jakich prac narzędzie sprawdza się najlepiej.</span>
                </div>
              </div>
            </div>

            <div class="app-tool-add-side-card app-tool-add-side-card-accent">
              <div class="text-overline mb-2">Co dalej</div>
              <h2 class="text-h6 font-weight-bold mb-2">Po zapisie przejdziesz od razu do strony oferty.</h2>
              <p class="mb-0 text-body-2 text-medium-emphasis">
                Dzięki temu od razu zobaczysz, jak narzędzie prezentuje się w serwisie i co warto ewentualnie poprawić.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="app-product-section">
        <div class="app-tool-add-form-shell">
          <ToolAddForm @tool-added="handleToolAdded" />
        </div>
      </section>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

import ToolAddForm from '@/features/tools/components/ToolAddForm.vue';
import type { Tool } from '@/types/tools';

const router = useRouter();

const handleToolAdded = async (tool: Tool): Promise<void> => {
  await router.push(`/tool/${tool.id}`);
};
</script>
