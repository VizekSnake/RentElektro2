<template>
  <div class="d-flex flex-column ga-4">
    <ResponseMessage
      v-if="successMessage"
      :message="successMessage"
      type="success"
      :showProgressBar="true"
      :duration="redirectDuration"
    />
    <ResponseMessage
      v-if="errorMessage"
      :message="errorMessage"
      type="error"
    />

    <v-form @submit.prevent="submitPasswordReset">
      <div class="d-flex flex-column ga-4">
        <AppTextField
          v-model="password"
          label="Nowe hasło"
          prepend-inner-icon="mdi-lock-outline"
          autocomplete="new-password"
          :type="showPassword ? 'text' : 'password'"
          :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
          required
          @click:append-inner="showPassword = !showPassword"
        />

        <AppTextField
          v-model="confirmPassword"
          label="Powtórz nowe hasło"
          prepend-inner-icon="mdi-lock-check-outline"
          autocomplete="new-password"
          :type="showConfirmPassword ? 'text' : 'password'"
          :append-inner-icon="showConfirmPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
          required
          @click:append-inner="showConfirmPassword = !showConfirmPassword"
        />

        <AppButton
          type="submit"
          size="large"
          :loading="isSubmitting"
          :disabled="!token || resetSuccessful"
          block
        >
          Ustaw nowe hasło
        </AppButton>
      </div>
    </v-form>

    <div class="text-body-2 text-medium-emphasis text-center">
      <router-link class="app-inline-link" to="/login">Wróć do logowania</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuth } from '@/composables/useAuth';
import { getApiErrorMessage } from '@/shared/api/apiErrors';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';

const route = useRoute();
const router = useRouter();
const { confirmReset, isSubmitting } = useAuth();
const password = ref('');
const confirmPassword = ref('');
const successMessage = ref('');
const errorMessage = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const resetSuccessful = ref(false);
const redirectDuration = 3000;

const token = computed(() => {
  const queryToken = route.query.token;
  return typeof queryToken === 'string' ? queryToken : '';
});

const submitPasswordReset = async (): Promise<void> => {
  successMessage.value = '';
  errorMessage.value = '';

  if (!token.value) {
    errorMessage.value = 'Brakuje tokenu resetu hasła. Otwórz link ponownie z wiadomości.';
    return;
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Hasła nie pasują do siebie.';
    return;
  }

  try {
    successMessage.value = await confirmReset({
      token: token.value,
      new_password: password.value,
    });
    resetSuccessful.value = true;
    window.setTimeout(() => {
      void router.push('/login');
    }, redirectDuration);
  } catch (error) {
    errorMessage.value = `Nie udało się ustawić nowego hasła: ${getApiErrorMessage(error, 'Nieznany błąd.')}`;
  }
};
</script>
