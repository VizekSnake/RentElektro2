<template>
  <section class="app-rental-inbox-card">
    <div class="d-flex flex-column flex-lg-row justify-space-between ga-4 mb-6">
      <div>
        <div class="text-overline mb-2">Centrum wynajmów</div>
        <h2 class="text-h5 font-weight-bold mb-2">Prośby, płatności i bieżące wypożyczenia</h2>
        <p class="app-muted-copy mb-0">
          Zarządzasz nowymi zgłoszeniami, opłacasz zaakceptowane wynajmy i śledzisz aktualne wydania oraz zwroty.
        </p>
      </div>
      <div class="d-flex flex-wrap ga-3">
        <div class="app-product-inline-meta">
          <span>Do decyzji</span>
          <strong>{{ ownerPendingRequests.length }}</strong>
        </div>
        <div class="app-product-inline-meta">
          <span>W toku</span>
          <strong>{{ ownerCurrentRentals.length + myCurrentRentals.length }}</strong>
        </div>
      </div>
    </div>

    <ResponseMessage v-if="successMessage" :message="successMessage" type="success" />
    <ResponseMessage v-if="errorMessage" :message="errorMessage" type="error" />

    <div v-if="isLoading" class="app-muted-copy">Ładowanie centrum wynajmów...</div>

    <template v-else>
      <div class="app-rental-board">
        <section class="app-rental-column">
          <div class="mb-4">
            <div class="text-overline mb-2">Jako właściciel</div>
            <h3 class="text-h6 font-weight-bold mb-1">Nowe prośby o wynajem</h3>
            <p class="app-muted-copy mb-0">Po akceptacji lub odrzuceniu zgłoszenie trafi do dalszego procesu.</p>
          </div>

          <div v-if="ownerPendingRequests.length === 0" class="app-rental-inbox-empty">
            Brak nowych próśb wymagających decyzji.
          </div>

          <v-expansion-panels v-else class="app-rental-panels" variant="accordion">
            <v-expansion-panel
              v-for="item in ownerPendingRequests"
              :key="`owner-pending-${item.id}`"
              class="app-rental-panel"
            >
              <v-expansion-panel-title>
                <div class="app-rental-panel-title">
                  <div class="d-flex align-center ga-3">
                    <v-avatar size="64" rounded="xl" class="app-rental-inbox-avatar">
                      <v-img :src="item.tool.ImageURL || ''" cover />
                    </v-avatar>
                    <div>
                      <div class="font-weight-bold">{{ item.tool.Brand }} {{ item.tool.TypeLabel || item.tool.Type }}</div>
                      <div class="app-muted-copy">{{ displayPerson(item.requester) }}</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="font-weight-bold">{{ formatRange(item.start_date, item.end_date) }}</div>
                    <div class="app-muted-copy">{{ rateLabel(item.tool.RatePerDay) }}</div>
                  </div>
                </div>
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <div class="app-rental-detail-grid">
                  <div class="app-rental-detail-card">
                    <span>Kto wypożycza</span>
                    <strong>{{ displayPerson(item.requester) }}</strong>
                    <div>{{ item.requester.email }}</div>
                    <div>{{ item.requester.phone || 'Brak telefonu' }}</div>
                  </div>
                  <div class="app-rental-detail-card">
                    <span>Status</span>
                    <strong>{{ statusLabel(item.status) }}</strong>
                    <div>{{ paymentLabel(item) }}</div>
                  </div>
                </div>

                <div v-if="item.comment" class="app-rental-inbox-note mt-4">
                  <div class="text-caption text-medium-emphasis mb-1">Komentarz najemcy</div>
                  <div>{{ item.comment }}</div>
                </div>

                <div class="mt-4">
                  <AppTextarea
                    :model-value="ownerComments[item.id] ?? item.owner_comment ?? ''"
                    label="Komentarz właściciela"
                    rows="3"
                    auto-grow
                    @update:model-value="ownerComments[item.id] = String($event ?? '')"
                  />
                </div>

                <div class="d-flex flex-wrap justify-space-between align-center ga-3 mt-4">
                  <div class="text-caption text-medium-emphasis">ID zgłoszenia #{{ item.id }}</div>
                  <div class="d-flex flex-wrap ga-3">
                    <AppButton
                      color="secondary"
                      variant="outlined"
                      :loading="isSubmitting"
                      @click="submitDecision(item.id, 'rejected_by_owner')"
                    >
                      Odrzuć
                    </AppButton>
                    <AppButton
                      color="primary"
                      :loading="isSubmitting"
                      @click="submitDecision(item.id, 'accepted')"
                    >
                      Akceptuj
                    </AppButton>
                  </div>
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>

          <div class="mt-6">
            <div class="text-subtitle-2 font-weight-bold mb-3">Aktualne wynajmy</div>
            <div v-if="ownerCurrentRentals.length === 0" class="app-rental-inbox-empty">
              Brak aktywnych wynajmów po Twojej stronie.
            </div>
            <div v-else class="app-rental-table-shell">
              <v-table class="app-rental-table">
                <thead>
                  <tr>
                    <th>Narzędzie</th>
                    <th>Najemca</th>
                    <th>Odbiór</th>
                    <th>Oddanie</th>
                    <th>Płatność</th>
                    <th>Akcja</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in ownerCurrentRentals" :key="`owner-current-${item.id}`">
                    <td>{{ item.tool.Brand }} {{ item.tool.TypeLabel || item.tool.Type }}</td>
                    <td>{{ displayPerson(item.requester) }}</td>
                    <td>{{ item.start_date }}</td>
                    <td>{{ item.end_date }}</td>
                    <td>{{ paymentLabel(item) }}</td>
                    <td>
                      <AppButton
                        v-if="item.is_paid && !item.handed_over_at"
                        size="small"
                        :loading="isSubmitting"
                        @click="advanceRentalStatus(item.id, 'paid_rented')"
                      >
                        Oznacz odbiór
                      </AppButton>
                      <AppButton
                        v-else-if="item.handed_over_at && !item.returned_at"
                        size="small"
                        variant="outlined"
                        color="secondary"
                        :loading="isSubmitting"
                        @click="advanceRentalStatus(item.id, 'fulfilled')"
                      >
                        Potwierdź zwrot
                      </AppButton>
                      <span v-else class="app-muted-copy">Bez akcji</span>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>
          </div>

          <div class="mt-6">
            <div class="text-subtitle-2 font-weight-bold mb-3">Moje narzędzia</div>
            <div v-if="myTools.length === 0" class="app-rental-inbox-empty">
              Nie masz jeszcze dodanych narzędzi.
            </div>
            <div v-else class="app-rental-table-shell">
              <v-table class="app-rental-table">
                <thead>
                  <tr>
                    <th>Narzędzie</th>
                    <th>Zasilanie</th>
                    <th>Cena / dzień</th>
                    <th>Status oferty</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="tool in myTools" :key="`my-tool-${tool.id}`">
                    <td>{{ tool.Brand }} {{ tool.TypeLabel || tool.Type }}</td>
                    <td>{{ tool.PowerSourceLabel || tool.PowerSource }}</td>
                    <td>{{ rateLabel(tool.RatePerDay) }}</td>
                    <td>
                      <div class="d-flex align-center justify-space-between ga-3">
                        <span>{{ toolAvailabilityLabel(tool.Availability) }}</span>
                        <AppButton
                          size="small"
                          variant="text"
                          :to="{ name: 'ToolProfileView', params: { id: tool.id } }"
                        >
                          Otwórz
                        </AppButton>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>
          </div>

          <div class="mt-6">
            <div class="text-subtitle-2 font-weight-bold mb-3">Archiwalne wynajmy jako właściciel</div>
            <div v-if="ownerHistoryRequests.length === 0" class="app-rental-inbox-empty">
              Archiwalne sprawy po stronie właściciela pojawią się tutaj po zakończeniu lub odrzuceniu pierwszego wynajmu.
            </div>
            <div v-else class="app-rental-table-shell">
              <v-table class="app-rental-table">
                <thead>
                  <tr>
                    <th>Narzędzie</th>
                    <th>Najemca</th>
                    <th>Termin</th>
                    <th>Status</th>
                    <th>Zwrot</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in ownerHistoryRequests" :key="`owner-history-${item.id}`">
                    <td>{{ item.tool.Brand }} {{ item.tool.TypeLabel || item.tool.Type }}</td>
                    <td>{{ displayPerson(item.requester) }}</td>
                    <td>{{ formatRange(item.start_date, item.end_date) }}</td>
                    <td>{{ archiveStatusLabel(item) }}</td>
                    <td>{{ returnLabel(item) }}</td>
                  </tr>
                </tbody>
              </v-table>
            </div>
          </div>
        </section>

        <section class="app-rental-column">
          <div class="mb-4">
            <div class="text-overline mb-2">Jako najemca</div>
            <h3 class="text-h6 font-weight-bold mb-1">Moje prośby i płatności</h3>
            <p class="app-muted-copy mb-0">Po akceptacji właściciela możesz od razu opłacić wynajem.</p>
          </div>

          <div v-if="myCurrentRentals.length === 0 && myPendingPaymentRequests.length === 0" class="app-rental-inbox-empty">
            Nie masz jeszcze aktywnych wynajmów ani płatności do wykonania.
          </div>

          <template v-else>
            <div v-if="myPendingPaymentRequests.length" class="mb-5">
              <div class="text-subtitle-2 font-weight-bold mb-3">Do opłacenia</div>
              <div class="app-rental-payment-list">
                <article
                  v-for="item in myPendingPaymentRequests"
                  :key="`payment-${item.id}`"
                  class="app-rental-payment-card"
                >
                  <div class="d-flex flex-column flex-lg-row justify-space-between ga-4">
                    <div>
                      <div class="font-weight-bold text-h6 mb-1">{{ item.tool.Brand }} {{ item.tool.TypeLabel || item.tool.Type }}</div>
                      <div class="app-muted-copy mb-1">{{ displayPerson(item.owner) }}</div>
                      <div class="app-muted-copy">{{ formatRange(item.start_date, item.end_date) }}</div>
                    </div>
                    <div class="app-product-inline-meta">
                      <span>Do zapłaty</span>
                      <strong>{{ totalLabel(item) }}</strong>
                    </div>
                  </div>

                  <div v-if="item.owner_comment" class="app-rental-inbox-note mt-4">
                    <div class="text-caption text-medium-emphasis mb-1">Komentarz właściciela</div>
                    <div>{{ item.owner_comment }}</div>
                  </div>

                  <div class="app-rental-payment-form mt-4">
                    <AppTextField
                      :model-value="paymentForms[item.id]?.cardholder ?? ''"
                      label="Imię i nazwisko na karcie"
                      prepend-inner-icon="mdi-account-outline"
                      @update:model-value="updatePaymentField(item.id, 'cardholder', $event)"
                    />
                    <AppTextField
                      :model-value="paymentForms[item.id]?.card_number ?? ''"
                      label="Numer karty"
                      prepend-inner-icon="mdi-credit-card-outline"
                      @update:model-value="updatePaymentField(item.id, 'card_number', $event)"
                    />
                    <AppTextField
                      :model-value="paymentForms[item.id]?.expiry_date ?? ''"
                      label="Data ważności"
                      prepend-inner-icon="mdi-calendar-month-outline"
                      @update:model-value="updatePaymentField(item.id, 'expiry_date', $event)"
                    />
                    <AppTextField
                      :model-value="paymentForms[item.id]?.cvc ?? ''"
                      label="CVC"
                      prepend-inner-icon="mdi-shield-lock-outline"
                      @update:model-value="updatePaymentField(item.id, 'cvc', $event)"
                    />
                  </div>

                  <div class="d-flex justify-end mt-4">
                    <AppButton :loading="isSubmitting" @click="submitPayment(item.id)">
                      Zapłać i potwierdź wynajem
                    </AppButton>
                  </div>
                </article>
              </div>
            </div>

            <div v-if="myCurrentRentals.length" class="mb-5">
              <div class="text-subtitle-2 font-weight-bold mb-3">Aktualne wynajmy</div>
              <div class="app-rental-table-shell">
                <v-table class="app-rental-table">
                  <thead>
                    <tr>
                      <th>Narzędzie</th>
                      <th>Właściciel</th>
                      <th>Odbiór</th>
                      <th>Oddanie</th>
                      <th>Płatność</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in myCurrentRentals" :key="`my-current-${item.id}`">
                      <td>{{ item.tool.Brand }} {{ item.tool.TypeLabel || item.tool.Type }}</td>
                      <td>{{ displayPerson(item.owner) }}</td>
                      <td>{{ item.start_date }}</td>
                      <td>{{ item.end_date }}</td>
                    <td>{{ paymentLabel(item) }}</td>
                    <td>{{ returnLabel(item) }}</td>
                    </tr>
                  </tbody>
                </v-table>
              </div>
            </div>
          </template>

          <div class="mt-6">
            <div class="text-subtitle-2 font-weight-bold mb-3">Archiwalne wynajmy jako najemca</div>
            <div v-if="myHistoricalRequests.length === 0" class="app-rental-inbox-empty">
              Archiwalne sprawy po stronie najemcy pojawią się tutaj po zakończeniu pierwszego wynajmu.
            </div>
            <div v-else class="app-rental-table-shell">
              <v-table class="app-rental-table">
                <thead>
                  <tr>
                    <th>Narzędzie</th>
                    <th>Właściciel</th>
                    <th>Termin</th>
                    <th>Status</th>
                    <th>Zwrot</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in myHistoricalRequests" :key="`renter-history-${item.id}`">
                    <td>{{ item.tool.Brand }} {{ item.tool.TypeLabel || item.tool.Type }}</td>
                    <td>{{ displayPerson(item.owner) }}</td>
                    <td>{{ formatRange(item.start_date, item.end_date) }}</td>
                    <td>{{ archiveStatusLabel(item) }}</td>
                    <td>{{ returnLabel(item) }}</td>
                  </tr>
                </tbody>
              </v-table>
            </div>
          </div>
        </section>
      </div>
    </template>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive } from 'vue';

import { useRentalInbox } from '@/composables/useRentalInbox';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import AppTextarea from '@/shared/ui/atoms/AppTextarea.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';
import type { Rental, RentalInboxItem, RentalPaymentPayload } from '@/types/rentals';

const ownerComments = reactive<Record<number, string>>({});
const paymentForms = reactive<Record<number, RentalPaymentPayload>>({});
const {
  ownerInboxItems,
  myRequestItems,
  myTools,
  isLoading,
  isSubmitting,
  errorMessage,
  successMessage,
  loadInbox,
  updateDecision,
  submitPayment: submitRentalPayment,
  advanceOwnerRentalStatus,
} = useRentalInbox();

const currencyFormatter = new Intl.NumberFormat('pl-PL', {
  style: 'currency',
  currency: 'PLN',
  maximumFractionDigits: 2,
});

const pendingStatuses: Rental['status'][] = ['not_viewed', 'viewed'];
const ownerCurrentStatuses: Rental['status'][] = ['accepted', 'paid_not_rented', 'paid_rented'];
const renterCurrentStatuses: Rental['status'][] = ['paid_not_rented', 'paid_rented'];

const ownerPendingRequests = computed(() =>
  ownerInboxItems.value.filter((item) => pendingStatuses.includes(item.status)),
);

const ownerCurrentRentals = computed(() =>
  ownerInboxItems.value.filter((item) => ownerCurrentStatuses.includes(item.status)),
);

const ownerHistoryRequests = computed(() =>
  ownerInboxItems.value.filter((item) => !pendingStatuses.includes(item.status) && !ownerCurrentStatuses.includes(item.status)),
);

const myPendingPaymentRequests = computed(() =>
  myRequestItems.value.filter((item) => item.status === 'accepted' && !item.is_paid),
);

const myCurrentRentals = computed(() =>
  myRequestItems.value.filter((item) => item.is_paid && renterCurrentStatuses.includes(item.status)),
);

const myHistoricalRequests = computed(() =>
  myRequestItems.value.filter(
    (item) => item.status !== 'accepted' && !renterCurrentStatuses.includes(item.status),
  ),
);

const rateLabel = (value: number | null): string =>
  value == null ? 'Brak stawki' : `${currencyFormatter.format(value)}/dzień`;

const totalLabel = (item: RentalInboxItem): string => {
  if (item.tool.RatePerDay == null) {
    return 'Do ustalenia';
  }

  const start = new Date(item.start_date);
  const end = new Date(item.end_date);
  const milliseconds = end.getTime() - start.getTime();
  const days = Math.max(1, Math.ceil(milliseconds / (1000 * 60 * 60 * 24)));
  return currencyFormatter.format(days * item.tool.RatePerDay);
};

const displayPerson = (person: { firstname: string; lastname: string; username: string }): string => {
  const fullName = `${person.firstname} ${person.lastname}`.trim();
  return fullName || person.username;
};

const toolAvailabilityLabel = (value: boolean): string => (value ? 'Dostępne' : 'Niedostępne');

const archiveStatusLabel = (item: RentalInboxItem): string =>
  item.status === 'fulfilled' ? 'Zakończone' : statusLabel(item.status);

const formatRange = (startDate: string, endDate: string): string => `${startDate} → ${endDate}`;

const statusLabel = (status: Rental['status']): string => {
  const labels: Record<Rental['status'], string> = {
    accepted: 'Zaakceptowane',
    rejected_by_owner: 'Odrzucone',
    canceled: 'Anulowane',
    fulfilled: 'Zwrócone',
    paid_rented: 'Wydane i opłacone',
    paid_not_rented: 'Opłacone',
    viewed: 'Odczytane',
    not_viewed: 'Nowe',
    problem: 'Problem',
    scam: 'Scam',
  };
  return labels[status];
};

const paymentLabel = (item: Pick<RentalInboxItem, 'status' | 'is_paid' | 'paid_at'>): string => {
  if (!item.is_paid && item.status === 'accepted') return 'Czeka na płatność';
  if (!item.is_paid) return 'Nieopłacone';
  if (item.paid_at) return `Opłacone ${item.paid_at.slice(0, 10)}`;
  return 'Opłacone';
};

const returnLabel = (
  item: Pick<RentalInboxItem, 'status' | 'is_paid' | 'handed_over_at' | 'returned_at'>,
): string => {
  if (item.returned_at || item.status === 'fulfilled') return 'Zwrócone';
  if (item.handed_over_at) return 'Sprzęt jest u najemcy';
  if (item.is_paid) return 'Czeka na odbiór';
  if (item.status === 'accepted') return 'Po akceptacji';
  if (item.status === 'rejected_by_owner' || item.status === 'canceled' || item.status === 'scam') return 'Nie dotyczy';
  return 'W trakcie';
};

const updatePaymentField = (
  rentalId: number,
  field: keyof RentalPaymentPayload,
  value: string | number | null,
): void => {
  if (!paymentForms[rentalId]) {
    paymentForms[rentalId] = {
      cardholder: '',
      card_number: '',
      expiry_date: '',
      cvc: '',
    };
  }

  paymentForms[rentalId][field] = typeof value === 'string' ? value : value == null ? '' : String(value);
};

const submitDecision = async (
  rentalId: number,
  status: 'accepted' | 'rejected_by_owner',
): Promise<void> => {
  await updateDecision(rentalId, {
    status,
    owner_comment: ownerComments[rentalId] ?? '',
  });
};

const submitPayment = async (rentalId: number): Promise<void> => {
  const form = paymentForms[rentalId];
  if (!form) {
    return;
  }

  await submitRentalPayment(rentalId, form);
};

const advanceRentalStatus = async (
  rentalId: number,
  status: 'paid_rented' | 'fulfilled',
): Promise<void> => {
  await advanceOwnerRentalStatus(rentalId, { status });
};

onMounted(() => {
  void loadInbox();
});
</script>
