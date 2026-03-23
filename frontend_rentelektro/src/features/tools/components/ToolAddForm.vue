<template>
  <div class="d-flex flex-column ga-5">
    <ResponseMessage v-if="successMessage" :message="successMessage" type="success" />
    <ResponseMessage v-if="errorMessage" :message="errorMessage" type="error" />

    <v-form ref="formRef" @submit.prevent="addTool">
      <div class="d-flex flex-column ga-6">
        <FormSection
          title="Podstawowe informacje"
          description="Nazwa, marka i opis budują pierwsze wrażenie oferty."
        >
          <v-row>
            <v-col cols="12" md="6">
              <AppTextField
                v-model="tool.Type"
                label="Typ narzędzia"
                prepend-inner-icon="mdi-hammer-screwdriver"
                :rules="requiredRule('Typ narzędzia')"
              />
            </v-col>
            <v-col cols="12" md="6">
              <AppTextField
                v-model="tool.Brand"
                label="Marka"
                prepend-inner-icon="mdi-tag-outline"
                :rules="requiredRule('Marka')"
              />
            </v-col>
            <v-col cols="12" md="6">
              <AppSelect
                v-model="tool.PowerSource"
                label="Źródło zasilania"
                :items="powerSources"
                prepend-inner-icon="mdi-power-plug-outline"
                :rules="requiredRule('Źródło zasilania')"
              />
            </v-col>
            <v-col cols="12" md="6">
              <AppSelect
                v-model="tool.category_id"
                label="Kategoria"
                :items="categoryOptions"
                item-title="title"
                item-value="value"
                prepend-inner-icon="mdi-shape-outline"
                :loading="isLoadingCategories"
                :disabled="isLoadingCategories || categoryOptions.length === 0"
                :hint="categoryHint"
                persistent-hint
                :rules="requiredRule('Kategoria')"
              />
            </v-col>
            <v-col cols="12">
              <AppTextarea
                v-model="tool.Description"
                label="Opis"
                prepend-inner-icon="mdi-text-box-outline"
                :rules="requiredRule('Opis')"
                rows="4"
                auto-grow
              />
            </v-col>
          </v-row>
        </FormSection>

        <FormSection
          title="Parametry techniczne"
          description="Podaj dane potrzebne do oceny stanu i opłacalności wynajmu."
        >
          <v-row>
            <v-col cols="12" md="4">
              <AppTextField
                v-model.number="tool.Power"
                label="Moc"
                type="number"
                prepend-inner-icon="mdi-flash-outline"
                :rules="requiredRule('Moc')"
              />
            </v-col>
            <v-col cols="12" md="4">
              <AppTextField
                v-model.number="tool.Age"
                label="Wiek"
                type="number"
                step="0.1"
                prepend-inner-icon="mdi-timer-sand"
                :rules="requiredRule('Wiek')"
              />
            </v-col>
            <v-col cols="12" md="4">
              <AppTextField
                v-model.number="tool.RatePerDay"
                label="Cena za dzień"
                type="number"
                step="0.01"
                prefix="PLN"
                prepend-inner-icon="mdi-cash"
                :rules="requiredRule('Cena za dzień')"
              />
            </v-col>
          </v-row>

          <ImageDropzone
            v-model="tool.ImageURL"
            :rules="requiredRule('Zdjęcie')"
            @invalid-file="errorMessage = $event"
          />
        </FormSection>

        <FormSection
          title="Status oferty"
          description="Zaznacz, czy narzędzie jest już dostępne i czy ma ubezpieczenie."
        >
          <div class="d-flex flex-column flex-md-row ga-4">
            <AppCheckbox v-model="tool.Availability" label="Dostępne od razu" hide-details />
            <AppCheckbox v-model="tool.Insurance" label="Objęte ubezpieczeniem" hide-details />
          </div>
        </FormSection>

        <div class="d-flex flex-column flex-sm-row ga-3">
          <AppButton type="submit" :loading="isSubmitting" prepend-icon="mdi-content-save-outline">
            Zapisz ofertę
          </AppButton>
          <AppButton variant="outlined" color="secondary" prepend-icon="mdi-refresh" @click="resetForm">
            Wyczyść formularz
          </AppButton>
        </div>
      </div>
    </v-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { VForm } from 'vuetify/components';
import { useToolForm } from '@/composables/useToolForm';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppCheckbox from '@/shared/ui/atoms/AppCheckbox.vue';
import AppSelect from '@/shared/ui/atoms/AppSelect.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import AppTextarea from '@/shared/ui/atoms/AppTextarea.vue';
import FormSection from '@/shared/ui/molecules/FormSection.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';
import ImageDropzone from '@/features/tools/components/ImageDropzone.vue';
import type { ToolFormPayload } from '@/types/tools';

const emit = defineEmits(['tool-added']);

const formRef = ref<VForm | null>(null);
const powerSources = ['electric', 'gas'];
const successMessage = ref('');
const {
  categoryOptions,
  categoryHint,
  isLoadingCategories,
  isSubmitting,
  errorMessage,
  fetchCategories,
  addTool: createToolOffer,
} = useToolForm();

const createInitialTool = (): ToolFormPayload => ({
  Type: '',
  PowerSource: '',
  Brand: '',
  Description: '',
  category_id: null,
  Availability: true,
  Insurance: false,
  Power: null,
  Age: null,
  RatePerDay: null,
  ImageURL: '',
});

const tool = ref<ToolFormPayload>(createInitialTool());

const requiredRule = (label: string) => [
  (value: string | number | null) => !!value || `${label} jest wymagane`,
];

const resetForm = (): void => {
  tool.value = createInitialTool();
  successMessage.value = '';
  errorMessage.value = '';
  formRef.value?.resetValidation();
};

const addTool = async (): Promise<void> => {
  const validationResult = await formRef.value?.validate();

  if (!validationResult?.valid) {
    return;
  }

  successMessage.value = '';

  try {
    await createToolOffer(tool.value);

    successMessage.value = 'Narzędzie zostało dodane do katalogu.';
    emit('tool-added');
    resetForm();
  } catch {
    return;
  }
};

void fetchCategories();
</script>
