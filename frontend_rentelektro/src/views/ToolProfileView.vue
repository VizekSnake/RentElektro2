<template>
  <v-container class="app-tool-profile">
    <ResponseMessage v-if="errorMessage" :message="errorMessage" type="error" />

    <DetailSplitSkeleton v-if="isLoading" />

    <template v-else>
      <section class="app-product-hero">
        <div class="app-product-hero-grid">
          <div class="app-product-media-shell">
            <ToolImage :image-url="toolData.ImageURL" />
          </div>

          <div class="d-flex flex-column ga-4">
            <div class="app-home-kicker">
              <v-icon size="18">mdi-star-four-points</v-icon>
              Oferta premium
            </div>

            <div class="d-flex flex-column ga-3">
              <div class="d-flex flex-wrap ga-2">
                <AppChip color="secondary" variant="flat">{{ toolData.Brand || 'Marka' }}</AppChip>
                <AppChip color="primary" variant="tonal">{{ toolData.PowerSourceLabel || toolData.PowerSource || 'Zasilanie' }}</AppChip>
                <AppChip :color="toolData.Availability ? 'success' : 'warning'" variant="tonal">
                  {{ toolData.Availability ? 'Dostępne' : 'Niedostępne' }}
                </AppChip>
              </div>

              <div>
                <h1 class="app-product-title ma-0">{{ toolData.TypeLabel || toolData.Type || 'Narzędzie' }}</h1>
                <p class="app-product-copy mt-3 mb-0">
                  {{ toolData.Description || 'Sprawdź szczegóły oferty, parametry techniczne i oszacuj koszt wynajmu.' }}
                </p>
              </div>
            </div>

            <div class="app-product-stat-strip">
              <div class="app-product-stat-card">
                <div class="app-product-stat-label">Cena za dzień</div>
                <div class="app-product-stat-value">{{ dailyRateLabel }}</div>
              </div>
              <div class="app-product-stat-card">
                <div class="app-product-stat-label">Moc</div>
                <div class="app-product-stat-value">{{ powerLabel }}</div>
              </div>
              <div class="app-product-stat-card">
                <div class="app-product-stat-label">Wiek</div>
                <div class="app-product-stat-value">{{ ageLabel }}</div>
              </div>
            </div>

            <div class="app-product-info-card">
              <ToolDetails :tool="toolData" />
            </div>
          </div>
        </div>
      </section>

      <section class="app-product-section">
        <div class="app-product-rental-card">
          <div class="d-flex flex-column flex-lg-row justify-space-between ga-4 mb-6">
            <div>
              <div class="text-overline mb-2">{{ isOwner ? 'Zarządzanie ofertą' : 'Wynajem' }}</div>
              <h2 class="text-h4 font-weight-bold mb-2">
                {{ isOwner ? 'Edytuj dane i kontroluj widoczność oferty' : 'Wybierz termin i wyślij prośbę' }}
              </h2>
              <p class="app-muted-copy mb-0">
                {{
                  isOwner
                    ? 'Z tego miejsca poprawisz szczegóły narzędzia i zdecydujesz, czy oferta ma być widoczna w publicznym katalogu.'
                    : 'Kalkulator jest osadzony w tej samej, lżejszej warstwie wizualnej co hero oferty.'
                }}
              </p>
            </div>
            <div class="app-product-inline-meta">
              <span>ID oferty</span>
              <strong>{{ toolData.public_id || 'n/d' }}</strong>
            </div>
          </div>

          <template v-if="isOwner">
            <ResponseMessage v-if="ownerErrorMessage" :message="ownerErrorMessage" type="error" />
            <ResponseMessage v-if="ownerSuccessMessage" :message="ownerSuccessMessage" type="success" />

            <v-form class="d-flex flex-column ga-5" @submit.prevent="saveOwnerChanges">
              <v-row>
                <v-col cols="12" md="6">
                  <AppTextField v-model="ownerForm.Brand" label="Marka" prepend-inner-icon="mdi-tag-outline" />
                </v-col>
                <v-col cols="12" md="6">
                  <AppTextField v-model="ownerForm.Type" label="Typ narzędzia" prepend-inner-icon="mdi-hammer-screwdriver" />
                </v-col>
                <v-col cols="12" md="4">
                  <AppTextField
                    v-model.number="ownerForm.Power"
                    label="Moc"
                    type="number"
                    prepend-inner-icon="mdi-flash-outline"
                  />
                </v-col>
                <v-col cols="12" md="4">
                  <AppTextField
                    v-model.number="ownerForm.Age"
                    label="Wiek"
                    type="number"
                    step="0.1"
                    prepend-inner-icon="mdi-timer-sand"
                  />
                </v-col>
                <v-col cols="12" md="4">
                  <AppTextField
                    v-model.number="ownerForm.RatePerDay"
                    label="Cena za dzień"
                    type="number"
                    step="0.01"
                    prefix="PLN"
                    prepend-inner-icon="mdi-cash"
                  />
                </v-col>
                <v-col cols="12">
                  <AppTextarea
                    v-model="ownerForm.Description"
                    label="Opis oferty"
                    rows="4"
                    auto-grow
                    prepend-inner-icon="mdi-text-box-outline"
                  />
                </v-col>
                <v-col cols="12">
                  <ImageDropzone
                    v-model="ownerForm.ImageURL"
                    input-label="Adres zdjęcia oferty"
                    input-hint="Możesz wkleić nowy publiczny URL albo sprawdzić lokalny podgląd przed zapisaniem."
                    @invalid-file="ownerErrorMessage = $event"
                  />
                </v-col>
                <v-col cols="12">
                  <div class="app-tool-owner-toggle">
                    <div>
                      <div class="font-weight-bold mb-1">Widoczność w katalogu</div>
                      <div class="app-muted-copy">
                        {{ ownerForm.Availability ? 'Oferta jest aktywna i widoczna publicznie.' : 'Oferta jest ukryta z publicznej listy.' }}
                      </div>
                    </div>
                    <AppButton
                      type="button"
                      :color="ownerForm.Availability ? 'secondary' : 'primary'"
                      :variant="ownerForm.Availability ? 'outlined' : 'flat'"
                      @click="toggleListing"
                    >
                      {{ ownerForm.Availability ? 'Wyłącz z listingu' : 'Przywróć do listingu' }}
                    </AppButton>
                  </div>
                </v-col>
              </v-row>

              <div class="d-flex justify-end">
                <AppButton type="submit" :loading="isSavingOwnerChanges">Zapisz zmiany</AppButton>
              </div>
            </v-form>
          </template>
          <RentalCalculator v-else :tool-id="toolData.id" :rate-per-day="toolData.RatePerDay ?? 0" />
        </div>
      </section>
    </template>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useToolDetails } from '@/composables/useToolDetails';
import { getSessionUser } from '@/services/authService';
import { updateTool } from '@/services/toolService';
import { useRoute } from 'vue-router';
import type { UUID } from '@/types/identifiers';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppChip from '@/shared/ui/atoms/AppChip.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import AppTextarea from '@/shared/ui/atoms/AppTextarea.vue';
import DetailSplitSkeleton from '@/shared/ui/organisms/DetailSplitSkeleton.vue';
import ImageDropzone from '@/features/tools/components/ImageDropzone.vue';
import ToolImage from '@/features/tools/components/ToolImage.vue';
import ToolDetails from '@/features/tools/components/ToolDetails.vue';
import RentalCalculator from '@/features/tools/components/RentalCalculator.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';
import { createLogger } from '@/shared/lib/logger';

const route = useRoute();
const logger = createLogger('tool-profile-view');
const currentUserId = ref<UUID | null>(null);
const isSavingOwnerChanges = ref(false);
const ownerSuccessMessage = ref('');
const ownerErrorMessage = ref('');
const fallbackTool = {
  id: '' as UUID,
  public_id: '',
  Type: '',
  TypeLabel: '',
  PowerSource: '',
  PowerSourceLabel: '',
  CategoryName: '',
  Brand: '',
  Description: '',
  category_id: null,
  Availability: false,
  Insurance: false,
  Power: null,
  Age: null,
  RatePerDay: 0,
  ImageURL: '',
  owner_id: '' as UUID,
};
const ownerForm = reactive({
  Type: '',
  Brand: '',
  Description: '',
  Power: null as number | null,
  Age: null as number | null,
  RatePerDay: null as number | null,
  ImageURL: '',
  Availability: false,
});
const { tool, isLoading, errorMessage, fetchToolDetails: loadToolDetails } = useToolDetails();
const toolData = computed(() => tool.value ?? fallbackTool);
const isOwner = computed(() => Boolean(currentUserId.value && toolData.value.owner_id === currentUserId.value));
const currencyFormatter = new Intl.NumberFormat('pl-PL', {
  style: 'currency',
  currency: 'PLN',
  maximumFractionDigits: 2,
});
const dailyRateLabel = computed(() => currencyFormatter.format(toolData.value.RatePerDay ?? 0));
const powerLabel = computed(() => (toolData.value.Power ? `${toolData.value.Power} W` : 'n/d'));
const ageLabel = computed(() => (toolData.value.Age ? `${toolData.value.Age} roku` : 'n/d'));

watch(
  toolData,
  (value) => {
    ownerForm.Type = value.Type || '';
    ownerForm.Brand = value.Brand || '';
    ownerForm.Description = value.Description || '';
    ownerForm.Power = value.Power ?? null;
    ownerForm.Age = value.Age ?? null;
    ownerForm.RatePerDay = value.RatePerDay ?? null;
    ownerForm.ImageURL = value.ImageURL || '';
    ownerForm.Availability = value.Availability;
  },
  { immediate: true },
);

const fetchToolDetails = async (): Promise<void> => {
  const previousError = errorMessage.value;
  await loadToolDetails(String(route.params.id));
  if (errorMessage.value && errorMessage.value !== previousError) {
    logger.error('fetch_tool_details_failed', errorMessage.value);
  }
};

const saveOwnerChanges = async (): Promise<void> => {
  if (!isOwner.value) {
    return;
  }

  isSavingOwnerChanges.value = true;
  ownerSuccessMessage.value = '';

  try {
    await updateTool(toolData.value.id, {
      Type: ownerForm.Type,
      Brand: ownerForm.Brand,
      Description: ownerForm.Description,
      Power: ownerForm.Power,
      Age: ownerForm.Age,
      RatePerDay: ownerForm.RatePerDay,
      ImageURL: ownerForm.ImageURL,
      Availability: ownerForm.Availability,
    });
    ownerSuccessMessage.value = ownerForm.Availability
      ? 'Oferta została zaktualizowana i pozostaje widoczna w katalogu.'
      : 'Oferta została zaktualizowana i ukryta z publicznej listy.';
    await fetchToolDetails();
  } catch (error) {
    ownerErrorMessage.value = error instanceof Error ? error.message : 'Nie udało się zapisać zmian w ofercie.';
  } finally {
    isSavingOwnerChanges.value = false;
  }
};

const toggleListing = (): void => {
  ownerForm.Availability = !ownerForm.Availability;
};

onMounted(() => {
  void getSessionUser().then((user) => {
    currentUserId.value = user?.id ?? null;
  });
  void fetchToolDetails();
});
</script>
