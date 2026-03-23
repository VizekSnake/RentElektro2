<template>
  <PageSection
    title="O serwisie"
    subtitle="RentElektro rozwija sie jako aplikacja do zarzadzania wynajmem narzedzi i obslugi kont uzytkownikow."
  >
    <SectionCard title="Kierunek projektu">
      <p class="text-body-1 text-medium-emphasis mb-4">
        Frontend korzysta z Vue 3 i Vuetify, a backend z FastAPI. Obecny etap skupia sie na domknieciu flows uzytkownika i uporzadkowaniu warstwy UI.
      </p>
      <p class="text-body-1 text-medium-emphasis">
        Kolejny etap to dopracowanie widokow, lepszy podzial komponentow i dalsze usuwanie dlugu technicznego po stronie backendu.
      </p>
    </SectionCard>
  </PageSection>
</template>

<script setup lang="ts">
import PageSection from '@/shared/ui/organisms/PageSection.vue';
import SectionCard from '@/shared/ui/organisms/SectionCard.vue';
</script>
