<template>
  <div class="d-flex flex-column ga-4">
    <ResponseMessage :message="errorMessage" type="error" />

    <v-form @submit.prevent="login">
      <div class="d-flex flex-column ga-4">
        <AppTextField
          v-model="username"
          label="Nazwa użytkownika"
          prepend-inner-icon="mdi-account-outline"
          autocomplete="username"
          required
        />

        <AppTextField
          v-model="password"
          label="Hasło"
          prepend-inner-icon="mdi-lock-outline"
          autocomplete="current-password"
          :type="showPassword ? 'text' : 'password'"
          :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
          required
          @click:append-inner="showPassword = !showPassword"
        />

        <AppButton
          type="submit"
          size="large"
          :loading="isSubmitting"
          block
        >
          Zaloguj
        </AppButton>
      </div>
    </v-form>

    <div class="text-body-2 text-medium-emphasis text-center">
      Nie masz konta?
      <router-link class="app-inline-link" to="/signup">Zarejestruj się</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';
import eventBus from '@/eventBus';
import { getApiErrorMessage } from '@/shared/api/apiErrors';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';

const router = useRouter();
const { login: loginUser, isSubmitting } = useAuth();
const username = ref('');
const password = ref('');
const errorMessage = ref('');
const showPassword = ref(false);

const login = async (): Promise<void> => {
  errorMessage.value = '';
  try {
    await loginUser(username.value, password.value);
    eventBus.emit('login');
    await router.push('/home');
  } catch (error) {
    errorMessage.value = `Logowanie nie powiodło się: ${getApiErrorMessage(error, 'Nieznany błąd.')}`;
  }
};
</script>
