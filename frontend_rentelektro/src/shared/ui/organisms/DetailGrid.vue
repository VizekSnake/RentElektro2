<template>
  <v-row>
    <v-col
      v-for="item in items"
      :key="item.label"
      :cols="cols"
      :md="md"
    >
      <MetricItem
        :label="item.label"
        :value="item.value"
        :value-class="item.valueClass"
      />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import MetricItem from '@/shared/ui/molecules/MetricItem.vue';

export type DetailGridItem = {
  label: string;
  value: string | number;
  valueClass?: string;
};

withDefaults(defineProps<{
  items: DetailGridItem[];
  cols?: string | number;
  md?: string | number;
}>(), {
  cols: 6,
  md: 4,
});
</script>
