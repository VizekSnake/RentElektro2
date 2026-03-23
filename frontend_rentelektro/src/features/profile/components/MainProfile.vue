<template>
  <v-container>
    <ResponseMessage v-if="errorMessage" :message="errorMessage" type="error" />

    <v-row v-if="user">
      <v-col cols="12">
        <ProfileOverview :user="user" />
      </v-col>
      <v-col cols="12">
        <ProfileEdit :user="user" @update-profile="handleUpdateProfile" />
      </v-col>
      <v-col cols="12">
        <ProfileSettings />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useProfile } from '@/composables/useProfile';
import ProfileEdit from '@/features/profile/components/ProfileEdit.vue';
import ProfileOverview from '@/features/profile/components/ProfileOverview.vue';
import ProfileSettings from '@/features/profile/components/ProfileSettings.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';
import { createLogger } from '@/shared/lib/logger';
import type { UserProfileUpdate } from '@/types/profile';

const logger = createLogger('main-profile');
const { user, errorMessage, fetchUserData, saveProfile } = useProfile();

const handleUpdateProfile = async (updatedUser: UserProfileUpdate): Promise<void> => {
  const previousError = errorMessage.value;
  await saveProfile(updatedUser);

  if (errorMessage.value && errorMessage.value !== previousError) {
    logger.error('update_profile_failed', errorMessage.value);
  }
};

onMounted(() => {
  void fetchUserData();
});
</script>
