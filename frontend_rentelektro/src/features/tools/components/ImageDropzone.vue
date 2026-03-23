<template>
  <v-row>
    <v-col cols="12" md="7">
      <button
        type="button"
        class="app-image-dropzone"
        :class="{ 'is-dragging': isDragging }"
        @click="openFilePicker"
        @dragenter.prevent="isDragging = true"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="handleFileDrop"
      >
        <div class="app-dropzone-icon">
          <v-icon size="32">mdi-image-plus</v-icon>
        </div>
        <div class="text-subtitle-1 font-weight-bold">
          Przeciągnij zdjęcie tutaj albo kliknij, aby wybrać plik
        </div>
        <div class="text-body-2 text-medium-emphasis">
          Obraz zapisze się tymczasowo jako podgląd oferty. Możesz też wkleić adres URL poniżej.
        </div>
      </button>

      <input
        ref="fileInputRef"
        type="file"
        accept="image/*"
        class="app-visually-hidden"
        @change="handleFileChange"
      >
    </v-col>

    <v-col cols="12" md="5">
      <div class="app-image-preview-shell">
        <v-img
          v-if="preview"
          :src="preview"
          class="rounded-lg"
          height="220"
          cover
        />
        <div v-else class="app-image-preview-placeholder">
          <v-icon size="40" color="grey-darken-1">mdi-image-outline</v-icon>
          <div class="text-body-2 text-medium-emphasis">Podgląd zdjęcia pojawi się tutaj</div>
        </div>
      </div>
    </v-col>

    <v-col cols="12">
      <AppTextField
        :model-value="modelValue"
        label="Adres zdjęcia lub wynik drag and drop"
        prepend-inner-icon="mdi-link-variant"
        :rules="rules"
        hint="Możesz wkleić URL albo wrzucić plik powyżej."
        persistent-hint
        @update:model-value="emit('update:modelValue', normalizeString($event))"
      />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';

const props = defineProps<{
  modelValue: string;
  rules?: unknown[];
}>();

const emit = defineEmits<{
  'update:modelValue': [value: string];
  invalidFile: [message: string];
}>();

const fileInputRef = ref<HTMLInputElement | null>(null);
const isDragging = ref(false);
const preview = ref(props.modelValue || '');

watch(
  () => props.modelValue,
  (value) => {
    preview.value = value || '';
  },
);

const normalizeString = (value: string | number | null): string =>
  typeof value === 'string' ? value : value == null ? '' : String(value);

const openFilePicker = (): void => {
  fileInputRef.value?.click();
};

const readImageFile = (file: File): void => {
  if (!file.type.startsWith('image/')) {
    emit('invalidFile', 'Możesz dodać tylko plik graficzny.');
    return;
  }

  const reader = new FileReader();
  reader.onload = () => {
    const result = typeof reader.result === 'string' ? reader.result : '';
    preview.value = result;
    emit('update:modelValue', result);
  };
  reader.readAsDataURL(file);
};

const handleFileChange = (event: Event): void => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (file) {
    readImageFile(file);
  }
};

const handleFileDrop = (event: DragEvent): void => {
  isDragging.value = false;
  const file = event.dataTransfer?.files?.[0];
  if (file) {
    readImageFile(file);
  }
};
</script>
