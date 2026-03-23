<template>
  <PageSection
    title="RentElektro"
    subtitle="Platforma do wynajmu elektronarzedzi z naciskiem na prosty onboarding, profile uzytkownikow i szybka obsluge ofert."
  >
    <v-row>
      <v-col cols="12" md="7">
        <SectionCard class="app-hero-panel">
          <HeroPanel
            title="Wynajem narzedzi bez chaosu"
            subtitle="Jeden katalog, czytelne profile i szybkie przejscie od ogloszenia do kalkulacji kosztu."
            panel-class="d-flex flex-column ga-6 position-relative"
            title-class="text-h4 font-weight-black"
            subtitle-class="text-body-1 text-white text-opacity-80 app-hero-copy mt-0 mb-0"
            content-class=""
            side-class="d-flex flex-column ga-6"
          >
            <template #actions>
              <div class="d-flex flex-wrap ga-3">
                <AppButton to="/tools" color="secondary" prepend-icon="mdi-tools">Przegladaj narzedzia</AppButton>
                <AppButton to="/tool/add" variant="outlined" color="white" prepend-icon="mdi-plus-circle-outline">Dodaj narzedzie</AppButton>
              </div>
            </template>

            <v-row class="mt-2">
              <v-col cols="12" sm="4">
                <StatCard label="Flow" value="Auth + Oferta" />
              </v-col>
              <v-col cols="12" sm="4">
                <StatCard label="UI" value="Vue + Vuetify" />
              </v-col>
              <v-col cols="12" sm="4">
                <StatCard label="Backend" value="FastAPI API" />
              </v-col>
            </v-row>

            <p class="text-body-1 text-white text-opacity-80 app-hero-copy">
              Zaloguj sie, dodaj nowe narzedzie albo przejdz do listy ofert. Interfejs jest ustawiony pod jasne, szybkie sciezki zamiast panelowego przeładowania.
            </p>
          </HeroPanel>
        </SectionCard>
      </v-col>
      <v-col cols="12" md="5">
        <SectionCard title="Co juz jest" subtitle="Aktualny zakres projektu frontendowego.">
          <v-list density="comfortable" bg-color="transparent" class="app-feature-list">
            <v-list-item prepend-icon="mdi-account-check-outline" title="Autoryzacja JWT" subtitle="Logowanie, rejestracja i ochrona wybranych widokow." />
            <v-list-item prepend-icon="mdi-view-grid-outline" title="Lista i profil narzedzi" subtitle="Katalog ofert, karta produktu i kalkulator wynajmu." />
            <v-list-item prepend-icon="mdi-calendar-clock-outline" title="Modul wynajmu" subtitle="Bazowy przeplyw do budowania procesu rezerwacji." />
          </v-list>
        </SectionCard>
      </v-col>
    </v-row>
  </PageSection>
</template>

<script setup lang="ts">
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import StatCard from '@/shared/ui/molecules/StatCard.vue';
import HeroPanel from '@/shared/ui/organisms/HeroPanel.vue';
import PageSection from '@/shared/ui/organisms/PageSection.vue';
import SectionCard from '@/shared/ui/organisms/SectionCard.vue';
</script>
