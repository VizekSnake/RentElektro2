<template>
  <div class="app-profile-stack">
    <ResponseMessage v-if="errorMessage" :message="errorMessage" type="error" />

    <template v-if="user">
      <ProfileOverview :user="user" />

      <div class="app-profile-grid">
        <div class="app-profile-edit-card">
          <ProfileEdit :user="user" @update-profile="handleUpdateProfile" />
        </div>
        <div class="app-profile-settings-card">
          <ProfileSettings
            :is-submitting="isSubmitting"
            :password-success-message="passwordSuccessMessage"
            @change-password="handlePasswordChange"
            @anonymize="handleAccountAnonymize"
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useProfile } from '@/composables/useProfile';
import ProfileEdit from '@/features/profile/components/ProfileEdit.vue';
import ProfileOverview from '@/features/profile/components/ProfileOverview.vue';
import ProfileSettings from '@/features/profile/components/ProfileSettings.vue';
import ResponseMessage from '@/shared/ui/molecules/ResponseMessage.vue';
import { createLogger } from '@/shared/lib/logger';
import eventBus from '@/eventBus';
import type { AccountAnonymizePayload, PasswordChangePayload, UserProfileUpdate } from '@/types/profile';

const logger = createLogger('main-profile');
const router = useRouter();
const passwordSuccessMessage = ref('');
const { user, errorMessage, fetchUserData, saveProfile, updatePassword, anonymizeCurrentAccount, isSubmitting } = useProfile();

const handleUpdateProfile = async (updatedUser: UserProfileUpdate): Promise<void> => {
  passwordSuccessMessage.value = '';
  const previousError = errorMessage.value;
  await saveProfile(updatedUser);

  if (errorMessage.value && errorMessage.value !== previousError) {
    logger.error('update_profile_failed', errorMessage.value);
  }
};

const handlePasswordChange = async (payload: PasswordChangePayload): Promise<void> => {
  passwordSuccessMessage.value = '';
  const success = await updatePassword(payload);
  if (success) {
    passwordSuccessMessage.value = 'Hasło zostało zaktualizowane.';
  }
};

const handleAccountAnonymize = async (payload: AccountAnonymizePayload): Promise<void> => {
  passwordSuccessMessage.value = '';
  const success = await anonymizeCurrentAccount(payload);
  if (!success) {
    return;
  }

  eventBus.emit('logout');
  await router.push('/login');
};

onMounted(() => {
  void fetchUserData();
});
</script>
