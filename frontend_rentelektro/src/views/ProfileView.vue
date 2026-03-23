<template>
  <PageSection
    title="Twoj profil"
    subtitle="Zarzadzaj danymi konta, ustawieniami i aktywnoscia zwiazana z wynajmami."
  >
    <SectionCard>
      <MainProfile />
    </SectionCard>
  </PageSection>
</template>

<script setup lang="ts">
import MainProfile from '@/features/profile/components/MainProfile.vue';
import PageSection from '@/shared/ui/organisms/PageSection.vue';
import SectionCard from '@/shared/ui/organisms/SectionCard.vue';
</script>
