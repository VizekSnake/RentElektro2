<template>
  <div class="app-profile-settings-shell">
    <div class="text-overline mb-2">Bezpieczeństwo</div>
    <h2 class="text-h5 font-weight-bold mb-2">Hasło i konto</h2>
    <p class="app-muted-copy mb-5">
      Tutaj zarządzasz dostępem do konta i decydujesz, czy chcesz je zanonimizować.
    </p>

    <div class="app-profile-settings-stack">
      <section class="app-profile-settings-block">
        <div class="mb-4">
          <div class="text-subtitle-1 font-weight-bold mb-1">Zmiana hasła</div>
          <div class="app-muted-copy">Podaj aktualne hasło i ustaw nowe dane logowania.</div>
        </div>

        <ResponseMessage v-if="passwordSuccessMessage" :message="passwordSuccessMessage" type="success" />

        <v-form @submit.prevent="submitPasswordChange">
          <div class="d-flex flex-column ga-4">
            <AppTextField
              v-model="passwordForm.current_password"
              label="Aktualne hasło"
              type="password"
              prepend-inner-icon="mdi-lock-outline"
            />
            <AppTextField
              v-model="passwordForm.new_password"
              label="Nowe hasło"
              type="password"
              prepend-inner-icon="mdi-shield-key-outline"
              hint="Minimum 8 znaków."
              persistent-hint
            />
            <div class="d-flex justify-end">
              <AppButton type="submit" :loading="isSubmitting">Zmień hasło</AppButton>
            </div>
          </div>
        </v-form>
      </section>

      <section class="app-profile-settings-block app-profile-settings-danger">
        <div class="mb-4">
          <div class="text-subtitle-1 font-weight-bold mb-1">Anonimizacja konta</div>
          <div class="app-muted-copy">
            Konto nie zostanie usunięte z bazy. Dane osobowe zostaną zastąpione anonimowymi wartościami, a dostęp do konta zostanie wyłączony.
          </div>
        </div>

        <AppTextField
          v-model="anonymizePassword"
          label="Potwierdź hasłem"
          type="password"
          prepend-inner-icon="mdi-alert-outline"
        />

        <div class="d-flex justify-end mt-4">
          <AppButton color="error" :loading="isSubmitting" @click="submitAnonymize">
            Zanonimizuj konto
          </AppButton>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';

import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';
import type { AccountAnonymizePayload, PasswordChangePayload } from '@/types/profile';

defineProps<{
  isSubmitting?: boolean;
  passwordSuccessMessage?: string;
}>();

const emit = defineEmits<{
  'change-password': [payload: PasswordChangePayload];
  anonymize: [payload: AccountAnonymizePayload];
}>();

const passwordForm = reactive<PasswordChangePayload>({
  current_password: '',
  new_password: '',
});

const anonymizePassword = ref('');

const submitPasswordChange = (): void => {
  emit('change-password', { ...passwordForm });
  passwordForm.current_password = '';
  passwordForm.new_password = '';
};

const submitAnonymize = (): void => {
  emit('anonymize', { current_password: anonymizePassword.value });
  anonymizePassword.value = '';
};
</script>
