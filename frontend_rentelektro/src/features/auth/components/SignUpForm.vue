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

    <v-form v-if="!registrationSuccessful" @submit.prevent="signup">
      <div class="d-flex flex-column ga-4">
        <AppTextField
          v-model="username"
          label="Nazwa użytkownika"
          prepend-inner-icon="mdi-account-outline"
          autocomplete="username"
          required
        />
        <AppTextField
          v-model="email"
          label="Adres email"
          prepend-inner-icon="mdi-email-outline"
          autocomplete="email"
          type="email"
          required
        />
        <AppTextField
          v-model="phone"
          label="Telefon"
          prepend-inner-icon="mdi-phone-outline"
          autocomplete="tel"
          required
        />
        <v-row>
          <v-col cols="12" md="6">
            <AppTextField
              v-model="firstname"
              label="Imię"
              autocomplete="given-name"
              required
            />
          </v-col>
          <v-col cols="12" md="6">
            <AppTextField
              v-model="lastname"
              label="Nazwisko"
              autocomplete="family-name"
              required
            />
          </v-col>
        </v-row>
        <AppCheckbox
          v-model="company"
          label="Konto firmowe"
          hide-details
        />
        <AppTextField
          v-model="password1"
          label="Hasło"
          prepend-inner-icon="mdi-lock-outline"
          autocomplete="new-password"
          :type="showPassword ? 'text' : 'password'"
          :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
          required
          @click:append-inner="showPassword = !showPassword"
        />
        <AppTextField
          v-model="password2"
          label="Powtórz hasło"
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
          block
        >
          Zarejestruj
        </AppButton>
      </div>
    </v-form>

    <div class="text-body-2 text-medium-emphasis text-center">
      Masz już konto?
      <router-link class="app-inline-link" to="/login">Zaloguj się</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';
import { getApiErrorMessage } from '@/shared/api/apiErrors';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppCheckbox from '@/shared/ui/atoms/AppCheckbox.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';

const router = useRouter();
const { signup: register, isSubmitting } = useAuth();
const username = ref('');
const email = ref('');
const phone = ref('');
const firstname = ref('');
const lastname = ref('');
const company = ref(false);
const password1 = ref('');
const password2 = ref('');
const successMessage = ref('');
const errorMessage = ref('');
const redirectDuration = 3000;
const registrationSuccessful = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const signup = async (): Promise<void> => {
  errorMessage.value = '';
  successMessage.value = '';
  isSubmitting.value = true;

  if (password1.value !== password2.value) {
    errorMessage.value = 'Hasła nie pasują do siebie';
    isSubmitting.value = false;
    return;
  }

  const formData = {
    username: username.value,
    email: email.value,
    phone: phone.value,
    firstname: firstname.value,
    lastname: lastname.value,
    company: company.value,
    password: password1.value,
  };

  try {
    await register(formData);

    successMessage.value = 'Rejestracja zakończona sukcesem!';
    registrationSuccessful.value = true;
    window.setTimeout(() => {
      void router.push('/login');
    }, redirectDuration);
  } catch (error) {
    errorMessage.value = `Rejestracja nie powiodła się: ${getApiErrorMessage(error, 'Nieznany błąd.')}`;
  }
};
</script>
