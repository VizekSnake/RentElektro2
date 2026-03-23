<template>
  <div class="d-flex flex-column ga-5">
    <ResponseMessage v-if="successMessage" :message="successMessage" type="success" />
    <ResponseMessage v-if="errorMessage" :message="errorMessage" type="error" />

    <v-row>
      <v-col cols="12" lg="7">
        <v-row>
          <v-col cols="12" md="6">
            <v-date-picker
              v-model="startDate"
              title="Data startu"
              hide-header
              elevation="0"
              class="app-calculator-picker"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-date-picker
              v-model="endDate"
              title="Data zakończenia"
              hide-header
              elevation="0"
              class="app-calculator-picker"
            />
          </v-col>
        </v-row>
      </v-col>

      <v-col cols="12" lg="5">
        <RentalSummaryCard
          :formatted-start-date="formattedStartDate"
          :formatted-end-date="formattedEndDate"
          :number-of-days="numberOfDays"
          :daily-rate-label="dailyRateLabel"
          :total-cost-label="totalCostLabel"
          :comment="comment"
          :is-submitting="isSubmitting"
          :can-submit="canSubmit"
          @update:comment="comment = $event"
          @submit="rentTool"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import RentalSummaryCard from '@/features/tools/components/RentalSummaryCard.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';
import { createRental, getCurrentUserId } from '@/services/rentalService';
import { createLogger } from '@/shared/lib/logger';

const props = defineProps<{
  toolId: number;
  ratePerDay: number;
}>();

const startDate = ref<string | null>(null);
const endDate = ref<string | null>(null);
const comment = ref('');
const currentUserId = ref<number | null>(null);
const isSubmitting = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const logger = createLogger('rental-calculator');

const currencyFormatter = new Intl.NumberFormat('pl-PL', {
  style: 'currency',
  currency: 'PLN',
  maximumFractionDigits: 2,
});

const numberOfDays = computed(() => {
  if (!startDate.value || !endDate.value) {
    return 0;
  }

  const start = new Date(startDate.value);
  const end = new Date(endDate.value);
  const diffTime = end.getTime() - start.getTime();
  if (diffTime < 0) {
    return 0;
  }
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
});

const totalCost = computed(() => numberOfDays.value * props.ratePerDay);
const dailyRateLabel = computed(() => currencyFormatter.format(props.ratePerDay || 0));
const totalCostLabel = computed(() => currencyFormatter.format(totalCost.value || 0));
const formattedStartDate = computed(() => startDate.value || 'Wybierz datę');
const formattedEndDate = computed(() => endDate.value || 'Wybierz datę');
const canSubmit = computed(
  () => Boolean(startDate.value && endDate.value && numberOfDays.value > 0 && currentUserId.value),
);

const formatDateForApi = (value: string): string => {
  const date = new Date(value);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}.${month}.${year}`;
};

const rentTool = async (): Promise<void> => {
  successMessage.value = '';
  errorMessage.value = '';

  if (!currentUserId.value) {
    errorMessage.value = 'Zaloguj się, aby wysłać prośbę o wynajem.';
    return;
  }

  if (!startDate.value || !endDate.value || numberOfDays.value <= 0) {
    errorMessage.value = 'Wybierz poprawny zakres dat.';
    return;
  }

  isSubmitting.value = true;

  try {
    await createRental({
      tool_id: props.toolId,
      user_id: currentUserId.value,
      start_date: formatDateForApi(startDate.value),
      end_date: formatDateForApi(endDate.value),
      comment: comment.value.trim(),
    });

    successMessage.value = 'Prośba o wynajem została wysłana.';
    logger.info('rental_request_created', { toolId: props.toolId, userId: currentUserId.value });
    comment.value = '';
  } catch (error) {
    logger.error('rental_request_failed', error);
    errorMessage.value = 'Nie udało się wysłać prośby o wynajem.';
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(async () => {
  currentUserId.value = await getCurrentUserId();
});
</script>
