<template>
  <div class="app-profile-form-shell">
    <div class="mb-6">
      <div class="text-overline mb-2">Edycja</div>
      <h2 class="text-h5 font-weight-bold mb-2">Edytuj profil</h2>
      <p class="app-muted-copy mb-0">
        Uzupełnij dane kontaktowe i ustaw publiczny wygląd swojego konta.
      </p>
    </div>

    <v-form @submit.prevent="updateProfile">
      <v-row>
        <v-col cols="12">
          <ImageDropzone
            v-model="form.profile_picture"
            title="Przeciągnij zdjęcie profilowe albo kliknij, aby wybrać plik"
            description="Możesz sprawdzić podgląd avatara przed zapisaniem zmian profilu."
            preview-placeholder="Podgląd zdjęcia profilowego pojawi się tutaj"
            input-label="Adres zdjęcia profilowego"
            input-hint="Wrzuć plik dla podglądu albo wklej publiczny URL avatara."
            local-file-notice="Plik lokalny służy tylko do podglądu. Aby zapisać avatar, wklej publiczny adres URL obrazka w polu poniżej."
            @invalid-file="imageMessage = $event"
          />
        </v-col>
        <v-col cols="12" md="6">
          <AppTextField
            v-model="form.username"
            label="Nazwa użytkownika"
            prepend-inner-icon="mdi-account"
          />
        </v-col>
        <v-col cols="12" md="6">
          <AppTextField
            v-model="form.email"
            label="Email"
            prepend-inner-icon="mdi-email"
            type="email"
          />
        </v-col>
        <v-col cols="12" md="6">
          <AppTextField
            v-model="form.firstname"
            label="Imię"
            prepend-inner-icon="mdi-account-outline"
          />
        </v-col>
        <v-col cols="12" md="6">
          <AppTextField
            v-model="form.lastname"
            label="Nazwisko"
            prepend-inner-icon="mdi-account-outline"
          />
        </v-col>
        <v-col cols="12" md="6">
          <AppTextField
            v-model="form.phone"
            label="Telefon"
            prepend-inner-icon="mdi-phone"
          />
        </v-col>
        <v-col cols="12" md="6" class="d-flex align-center">
          <AppCheckbox
            v-model="form.company"
            label="Konto firmowe"
          />
        </v-col>
      </v-row>
      <div class="mt-4">
        <AppButton type="submit" color="primary" size="large">Zaktualizuj dane</AppButton>
      </div>
    </v-form>
    <p v-if="imageMessage" class="app-muted-copy mt-4">{{ imageMessage }}</p>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppCheckbox from '@/shared/ui/atoms/AppCheckbox.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import ImageDropzone from '@/features/tools/components/ImageDropzone.vue';
import type { UserProfile, UserProfileUpdate } from '@/types/profile';

const props = defineProps<{
  user: UserProfile;
}>();

const emit = defineEmits(['update-profile']);
const imageMessage = ref('');

const form = reactive<UserProfileUpdate>({
  profile_picture: '',
  username: '',
  email: '',
  phone: '',
  firstname: '',
  lastname: '',
  company: false,
});

watch(
  () => props.user,
  (newUser) => {
    form.profile_picture = newUser.profile_picture;
    form.username = newUser.username;
    form.email = newUser.email;
    form.phone = newUser.phone;
    form.firstname = newUser.firstname;
    form.lastname = newUser.lastname;
    form.company = newUser.company;
  },
  { immediate: true },
);

const updateProfile = (): void => {
  emit('update-profile', { ...form });
};
</script>
