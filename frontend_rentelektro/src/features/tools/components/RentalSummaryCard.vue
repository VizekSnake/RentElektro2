<template>
  <div class="app-calculator-panel">
    <div class="text-overline text-medium-emphasis">Podsumowanie</div>
    <div class="text-h5 font-weight-bold mb-4">Policz koszt i wyślij zgłoszenie</div>

    <div class="app-summary-grid">
      <MetricItem
        v-for="item in summaryItems"
        :key="item.label"
        :label="item.label"
        :value="item.value"
      />
    </div>

    <v-divider class="my-4" />

    <div class="d-flex justify-space-between align-end mb-4">
      <MetricItem label="Łączny koszt" :value="totalCostLabel" value-class="text-h4 font-weight-black" />
      <AppChip color="secondary" variant="tonal">Szacunek brutto</AppChip>
    </div>

    <AppTextarea
      :model-value="comment"
      label="Komentarz do właściciela"
      rows="3"
      auto-grow
      placeholder="Np. potrzebuję narzędzia na weekendowy remont."
      @update:model-value="emit('update:comment', normalizeString($event))"
    />

    <AppButton
      class="mt-2"
      color="primary"
      size="large"
      block
      :loading="isSubmitting"
      :disabled="!canSubmit"
      @click="emit('submit')"
    >
      Wyślij prośbę o wynajem
    </AppButton>

    <p class="text-caption text-medium-emphasis mt-3 mb-0">
      Aby złożyć prośbę, wybierz poprawny zakres dat i zaloguj się do konta.
    </p>
  </div>
</template>

<script setup lang="ts">
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppChip from '@/shared/ui/atoms/AppChip.vue';
import AppTextarea from '@/shared/ui/atoms/AppTextarea.vue';
import MetricItem from '@/shared/ui/molecules/MetricItem.vue';

const props = defineProps<{
  formattedStartDate: string;
  formattedEndDate: string;
  numberOfDays: number;
  dailyRateLabel: string;
  totalCostLabel: string;
  comment: string;
  isSubmitting: boolean;
  canSubmit: boolean;
}>();

const emit = defineEmits<{
  'update:comment': [value: string];
  submit: [];
}>();

const summaryItems = [
  { label: 'Start', value: props.formattedStartDate },
  { label: 'Koniec', value: props.formattedEndDate },
  { label: 'Dni', value: props.numberOfDays },
  { label: 'Stawka', value: props.dailyRateLabel },
];

const normalizeString = (value: string | number | null): string =>
  typeof value === 'string' ? value : value == null ? '' : String(value);
</script>
