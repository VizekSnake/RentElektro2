import { ref } from 'vue';
import { anonymizeAccount, changePassword, fetchProfile, updateProfile } from '@/services/profileService';
import type {
  AccountAnonymizePayload,
  PasswordChangePayload,
  UserProfile,
  UserProfileUpdate,
} from '@/types/profile';

export function useProfile() {
  const user = ref<UserProfile | null>(null);
  const isLoading = ref(false);
  const isSubmitting = ref(false);
  const errorMessage = ref('');

  const fetchUserData = async (): Promise<void> => {
    isLoading.value = true;
    errorMessage.value = '';

    try {
      user.value = await fetchProfile();
    } catch {
      errorMessage.value = 'Nie udało się pobrać danych profilu.';
    } finally {
      isLoading.value = false;
    }
  };

  const saveProfile = async (updatedUser: UserProfileUpdate): Promise<void> => {
    if (!user.value) {
      return;
    }

    isSubmitting.value = true;
    errorMessage.value = '';

    try {
      await updateProfile(user.value.id, updatedUser);
      await fetchUserData();
    } catch {
      errorMessage.value = 'Nie udało się zaktualizować profilu.';
    } finally {
      isSubmitting.value = false;
    }
  };

  const updatePassword = async (payload: PasswordChangePayload): Promise<boolean> => {
    isSubmitting.value = true;
    errorMessage.value = '';

    try {
      await changePassword(payload);
      return true;
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : 'Nie udało się zmienić hasła.';
      return false;
    } finally {
      isSubmitting.value = false;
    }
  };

  const anonymizeCurrentAccount = async (payload: AccountAnonymizePayload): Promise<boolean> => {
    isSubmitting.value = true;
    errorMessage.value = '';

    try {
      await anonymizeAccount(payload);
      return true;
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : 'Nie udało się zanonimizować konta.';
      return false;
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    user,
    isLoading,
    isSubmitting,
    errorMessage,
    fetchUserData,
    saveProfile,
    updatePassword,
    anonymizeCurrentAccount,
  };
}
