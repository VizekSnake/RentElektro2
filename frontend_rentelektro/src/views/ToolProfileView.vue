<template>
  <PageSection
    title="Szczegoly narzedzia"
    subtitle="Podglad oferty, parametrow i szacunkowego kosztu wynajmu."
  >
    <HeroPanel
      class="mb-6"
      eyebrow="Oferta"
      :title="toolData.Type || 'Narzędzie'"
      :subtitle="toolData.Description || 'Sprawdź szczegóły oferty, parametry techniczne i oszacuj koszt wynajmu.'"
    >
      <template #tags>
        <AppChip color="secondary" variant="flat">{{ toolData.Brand || 'Marka' }}</AppChip>
        <AppChip color="primary" variant="tonal">{{ toolData.PowerSource || 'Zasilanie' }}</AppChip>
        <AppChip :color="toolData.Availability ? 'success' : 'warning'" variant="tonal">
        {{ toolData.Availability ? 'Dostepne' : 'Niedostepne' }}
        </AppChip>
      </template>
    </HeroPanel>

    <ResponseMessage v-if="errorMessage" :message="errorMessage" type="error" />

    <DetailSplitSkeleton v-if="isLoading" />

    <v-row v-else>
      <v-col cols="12" md="6">
        <SectionCard title="Galeria">
          <ToolImage :image-url="toolData.ImageURL" />
        </SectionCard>
      </v-col>
      <v-col cols="12" md="6">
        <SectionCard title="Opis">
          <ToolDetails :tool="toolData" />
        </SectionCard>
      </v-col>
    </v-row>
    <v-row v-if="!isLoading" class="mt-1 mt-md-3">
      <v-col cols="12">
        <SectionCard
          title="Kalkulator wynajmu"
          subtitle="Wybierz termin, policz koszt i od razu wyślij zgłoszenie do właściciela."
        >
          <RentalCalculator :tool-id="toolData.id" :rate-per-day="toolData.RatePerDay ?? 0" />
        </SectionCard>
      </v-col>
    </v-row>
  </PageSection>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useToolDetails } from '@/composables/useToolDetails';
import { useRoute } from 'vue-router';
import AppChip from '@/shared/ui/atoms/AppChip.vue';
import DetailSplitSkeleton from '@/shared/ui/organisms/DetailSplitSkeleton.vue';
import HeroPanel from '@/shared/ui/organisms/HeroPanel.vue';
import ToolImage from "@/features/tools/components/ToolImage.vue";
import ToolDetails from "@/features/tools/components/ToolDetails.vue";
import RentalCalculator from "@/features/tools/components/RentalCalculator.vue";
import PageSection from '@/shared/ui/organisms/PageSection.vue';
import SectionCard from '@/shared/ui/organisms/SectionCard.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';
import { createLogger } from '@/shared/lib/logger';

const route = useRoute();
const logger = createLogger('tool-profile-view');
const fallbackTool = {
  id: 0,
  Type: '',
  PowerSource: '',
  Brand: '',
  Description: '',
  category_id: null,
  Availability: false,
  Insurance: false,
  Power: null,
  Age: null,
  RatePerDay: 0,
  ImageURL: '',
};
const { tool, isLoading, errorMessage, fetchToolDetails: loadToolDetails } = useToolDetails();
const toolData = computed(() => tool.value ?? fallbackTool);

const fetchToolDetails = async (): Promise<void> => {
  const previousError = errorMessage.value;
  await loadToolDetails(String(route.params.id));
  if (errorMessage.value && errorMessage.value !== previousError) {
    logger.error('fetch_tool_details_failed', errorMessage.value);
  }
};

onMounted(() => {
  void fetchToolDetails();
});
</script>
