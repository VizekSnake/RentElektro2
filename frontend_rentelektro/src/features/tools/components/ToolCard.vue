<template>
  <v-card class="app-tool-card h-100 d-flex flex-column" border="sm">
    <v-img
      :src="tool.ImageURL"
      height="240"
      cover
      class="app-tool-image"
    >
      <div class="d-flex justify-space-between align-start pa-4 app-image-overlay">
        <AppChip color="secondary" variant="flat" size="small">
          {{ tool.PowerSource || 'n/a' }}
        </AppChip>
        <AppChip :color="tool.Availability ? 'success' : 'warning'" variant="tonal" size="small">
          {{ tool.Availability ? 'Dostępne' : 'Niedostępne' }}
        </AppChip>
      </div>
    </v-img>

    <v-card-item>
      <v-card-title class="text-wrap">{{ tool.Type }}</v-card-title>
      <v-card-subtitle>{{ tool.Brand }}</v-card-subtitle>
    </v-card-item>

    <v-card-text class="d-flex flex-column ga-4">
      <p class="text-body-2 text-medium-emphasis">
        {{ shortDescription }}
      </p>

      <div class="d-flex flex-wrap ga-2">
        <AppChip size="small" variant="tonal">Kategoria #{{ categoryId ?? 'n/a' }}</AppChip>
        <AppChip size="small" variant="tonal">Moc: {{ tool.Power ?? 'n/a' }}</AppChip>
        <AppChip size="small" variant="tonal">Wiek: {{ tool.Age ?? 'n/a' }}</AppChip>
      </div>

      <div class="d-flex justify-space-between align-center mt-auto">
        <div>
          <div class="text-caption text-medium-emphasis">Cena za dzień</div>
          <div class="text-h6 font-weight-bold">${{ displayRate }}</div>
        </div>
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

const displayRate = computed(() => props.tool.RatePerDay ?? 0);
const categoryId = computed(() => getToolCategoryId(props.tool));
</script>
