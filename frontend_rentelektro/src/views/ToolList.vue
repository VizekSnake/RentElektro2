<template>
  <PageSection
    title="Narzędzia"
    subtitle="Przeglądaj dostępny sprzęt i przechodź do pełnych szczegółów oferty."
  >
    <template #actions>
      <AppButton to="/tool/add" prepend-icon="mdi-plus-circle-outline">
        Dodaj narzędzie
      </AppButton>
    </template>

    <div class="mb-6 d-flex flex-wrap ga-3">
      <AppChip color="primary" variant="flat">Oferty: {{ tools.length }}</AppChip>
      <AppChip color="secondary" variant="tonal">Widok katalogu</AppChip>
      <AppChip color="primary" variant="tonal">Nowy modularny UI</AppChip>
    </div>

    <ResponseMessage v-if="errorMessage" :message="errorMessage" type="error" />

    <CardGridSkeleton v-if="isLoading" />

    <EmptyState
      v-else-if="tools.length === 0"
      title="Brak narzędzi"
      subtitle="Nie ma jeszcze żadnych ofert. Dodaj pierwsze narzędzie i zbuduj katalog."
    >
      <template #actions>
        <AppButton to="/tool/add" prepend-icon="mdi-hammer-wrench">
          Dodaj pierwsze narzędzie
        </AppButton>
      </template>
    </EmptyState>

    <v-row v-else>
      <v-col v-for="tool in tools" :key="tool.id" cols="12" md="6" lg="4">
        <ToolCard :tool="tool" />
      </v-col>
    </v-row>
  </PageSection>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useToolList } from '@/composables/useToolList';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppChip from '@/shared/ui/atoms/AppChip.vue';
import PageSection from '@/shared/ui/organisms/PageSection.vue';
import CardGridSkeleton from '@/shared/ui/organisms/CardGridSkeleton.vue';
import EmptyState from '@/shared/ui/organisms/EmptyState.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';
import ToolCard from '@/features/tools/components/ToolCard.vue';
import { createLogger } from '@/shared/lib/logger';

const { tools, isLoading, errorMessage, fetchTools: loadTools } = useToolList();
const logger = createLogger('tool-list-view');

const fetchTools = async (): Promise<void> => {
  const previousError = errorMessage.value;
  await loadTools();
  if (errorMessage.value && errorMessage.value !== previousError) {
    logger.error('fetch_tools_failed', errorMessage.value);
  }
};

onMounted(() => {
  void fetchTools();
});
</script>
