<template>
  <div class="d-flex flex-column ga-5">
    <div>
      <TagGroup class="mb-2" :tags="statusTags" />
      <h2 class="text-h4 font-weight-bold mb-1">{{ tool.TypeLabel || tool.Type }}</h2>
      <p class="text-body-1 text-medium-emphasis">{{ tool.Brand }}</p>
    </div>

    <p class="text-body-1">{{ tool.Description || 'Brak opisu narzędzia.' }}</p>

    <DetailGrid :items="detailItems" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import DetailGrid from '@/shared/ui/organisms/DetailGrid.vue';
import TagGroup, { type TagGroupItem } from '@/shared/ui/molecules/TagGroup.vue';
import type { Tool } from '@/types/tools';
import { getToolCategoryId } from '@/types/tools';

const props = defineProps<{
  tool: Tool;
}>();

const categoryId = computed(() => getToolCategoryId(props.tool));
const statusTags = computed<TagGroupItem[]>(() => {
  const items: TagGroupItem[] = [
    {
      label: props.tool.PowerSourceLabel || props.tool.PowerSource || 'n/a',
      color: 'secondary',
      variant: 'flat',
      size: 'small',
    },
    {
      label: props.tool.Availability ? 'Dostępne' : 'Niedostępne',
      color: props.tool.Availability ? 'success' : 'warning',
      variant: 'tonal',
      size: 'small',
    },
  ];

  if (props.tool.Insurance) {
    items.push({
      label: 'Ubezpieczone',
      color: 'primary',
      variant: 'tonal',
      size: 'small',
    });
  }

  return items;
});

const detailItems = computed(() => [
  { label: 'Kategoria', value: `#${categoryId.value ?? 'n/a'}` },
  { label: 'Moc', value: props.tool.Power ?? 'n/a' },
  { label: 'Wiek', value: props.tool.Age ?? 'n/a' },
  { label: 'Cena za dzień', value: `$${props.tool.RatePerDay ?? 0}`, valueClass: 'text-body-1 font-weight-bold' },
]);
</script>
