<template>
  <div class="d-flex flex-column ga-4">
    <ResponseMessage
      v-if="successMessage"
      :message="successMessage"
      type="success"
    />
    <ResponseMessage
      v-if="errorMessage"
      :message="errorMessage"
      type="error"
    />

    <v-form @submit.prevent="submitResetRequest">
      <div class="d-flex flex-column ga-4">
        <AppTextField
          v-model="email"
          label="Adres email"
          prepend-inner-icon="mdi-email-outline"
          autocomplete="email"
          type="email"
          required
        />

        <AppButton
          type="submit"
          size="large"
          :loading="isSubmitting"
          block
        >
          Wyślij link resetu
        </AppButton>
      </div>
    </v-form>

    <div class="text-body-2 text-medium-emphasis text-center">
      <router-link class="app-inline-link" to="/login">Wróć do logowania</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuth } from '@/composables/useAuth';
import { getApiErrorMessage } from '@/shared/api/apiErrors';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';

const { requestReset, isSubmitting } = useAuth();
const email = ref('');
const successMessage = ref('');
const errorMessage = ref('');

const submitResetRequest = async (): Promise<void> => {
  successMessage.value = '';
  errorMessage.value = '';

  try {
    successMessage.value = await requestReset({ email: email.value });
  } catch (error) {
    errorMessage.value = `Nie udało się wysłać linku resetu: ${getApiErrorMessage(error, 'Nieznany błąd.')}`;
  }
};
</script>
