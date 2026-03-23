<template>
  <PageSection
    title="Dodaj narzędzie"
    subtitle="Uzupełnij podstawowe parametry oferty, aby opublikować sprzęt w katalogu."
  >
    <SectionCard title="Nowa oferta" subtitle="Im lepszy opis i zdjęcie, tym czytelniejsza karta produktu.">
      <ToolAddForm @tool-added="handleToolAdded" />
    </SectionCard>
  </PageSection>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import ToolAddForm from '@/features/tools/components/ToolAddForm.vue';
import PageSection from '@/shared/ui/organisms/PageSection.vue';
import SectionCard from '@/shared/ui/organisms/SectionCard.vue';

const router = useRouter();

const handleToolAdded = async (): Promise<void> => {
  await router.push('/tools');
};
</script>
