<template>
  <v-card class="app-tool-card h-100 d-flex flex-column" border="sm">
    <v-img
      :src="tool.ImageURL"
      height="260"
      cover
      class="app-tool-image"
    >
      <div class="d-flex justify-space-between align-start pa-4 app-image-overlay">
        <AppChip color="secondary" variant="flat" size="small">
          {{ tool.PowerSourceLabel || tool.PowerSource || 'n/d' }}
        </AppChip>
        <AppChip :color="tool.Availability ? 'success' : 'warning'" variant="tonal" size="small">
          {{ tool.Availability ? 'Dostępne' : 'Niedostępne' }}
        </AppChip>
      </div>
    </v-img>

    <v-card-text class="d-flex flex-column ga-4 pa-5">
      <div class="d-flex justify-space-between align-start ga-4">
        <div>
          <div class="text-caption text-medium-emphasis mb-1">{{ tool.Brand }}</div>
          <h3 class="text-h5 font-weight-bold mb-0">{{ tool.TypeLabel || tool.Type }}</h3>
        </div>
        <div class="app-tool-card-price">
          <span>za dzień</span>
          <strong>{{ displayRate }}</strong>
        </div>
      </div>

      <p class="text-body-2 text-medium-emphasis mb-0">
        {{ shortDescription }}
      </p>

      <div class="app-tool-card-meta">
        <div class="app-tool-card-meta-item">
          <span>Kategoria</span>
          <strong>#{{ categoryId ?? 'n/d' }}</strong>
        </div>
        <div class="app-tool-card-meta-item">
          <span>Moc</span>
          <strong>{{ powerLabel }}</strong>
        </div>
        <div class="app-tool-card-meta-item">
          <span>Wiek</span>
          <strong>{{ ageLabel }}</strong>
        </div>
      </div>

      <div class="d-flex justify-space-between align-center mt-auto pt-2">
        <div class="text-caption text-medium-emphasis">Szybki podgląd oferty</div>
        <AppButton :to="{ name: 'ToolProfileView', params: { id: tool.id } }" prepend-icon="mdi-arrow-right">
          Szczegóły
        </AppButton>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppChip from '@/shared/ui/atoms/AppChip.vue';
import type { Tool } from '@/types/tools';
import { getToolCategoryId } from '@/types/tools';

const props = defineProps<{
  tool: Tool;
}>();

const shortDescription = computed(() => {
  if (!props.tool.Description) {
    return 'Brak opisu narzędzia.';
  }

  return props.tool.Description.length > 120
    ? `${props.tool.Description.slice(0, 117)}...`
    : props.tool.Description;
});

const currencyFormatter = new Intl.NumberFormat('pl-PL', {
  style: 'currency',
  currency: 'PLN',
  maximumFractionDigits: 2,
});
const displayRate = computed(() => currencyFormatter.format(props.tool.RatePerDay ?? 0));
const categoryId = computed(() => getToolCategoryId(props.tool));
const powerLabel = computed(() => (props.tool.Power ? `${props.tool.Power} W` : 'n/d'));
const ageLabel = computed(() => (props.tool.Age ? `${props.tool.Age} roku` : 'n/d'));
</script>
