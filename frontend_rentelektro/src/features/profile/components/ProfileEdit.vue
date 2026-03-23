<template>
  <v-container class="app-profile-edit" max-width="600px">
    <v-card>
      <v-card-title>
        <h2>Edytuj profil</h2>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateProfile">
          <v-row>
            <v-col cols="12">
              <AppTextField
                v-model="form.profile_picture"
                label="Zdjęcie profilowe"
                prepend-inner-icon="mdi-camera"
              />
            </v-col>
            <v-col cols="12">
              <AppTextField
                v-model="form.username"
                label="Nazwa użytkownika"
                prepend-inner-icon="mdi-account"
              />
            </v-col>
            <v-col cols="12">
              <AppTextField
                v-model="form.firstname"
                label="Imię"
                prepend-inner-icon="mdi-account"
              />
            </v-col>
            <v-col cols="12">
              <AppTextField
                v-model="form.lastname"
                label="Nazwisko"
                prepend-inner-icon="mdi-account"
              />
            </v-col>
            <v-col cols="12">
              <AppTextField
                v-model="form.phone"
                label="Telefon"
                prepend-inner-icon="mdi-phone"
              />
            </v-col>
            <v-col cols="12">
              <AppCheckbox
                v-model="form.company"
                label="Użytkownik biznesowy"
              />
            </v-col>
            <v-col cols="12">
              <AppTextField
                v-model="form.email"
                label="Email"
                prepend-inner-icon="mdi-email"
                type="email"
              />
            </v-col>
          </v-row>
          <v-card-actions>
            <AppButton type="submit" color="primary">Zaktualizuj dane</AppButton>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import AppCheckbox from '@/shared/ui/atoms/AppCheckbox.vue';
import AppTextField from '@/shared/ui/atoms/AppTextField.vue';
import type { UserProfile, UserProfileUpdate } from '@/types/profile';

const props = defineProps<{
  user: UserProfile;
}>();

const emit = defineEmits(['update-profile']);

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
