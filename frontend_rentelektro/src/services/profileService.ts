import apiClient from '@/shared/api/apiClient';
import { assertApiResponse, unwrapApiResponse } from '@/shared/api/apiErrors';
import type {
  AccountAnonymizePayload,
  PasswordChangePayload,
  UserProfile,
  UserProfileUpdate,
} from '@/types/profile';

export async function fetchProfile(): Promise<UserProfile> {
  const response = await apiClient.GET('/users/me/data');
  return unwrapApiResponse(response, 'Nie udało się pobrać profilu.');
}

export async function updateProfile(userId: number, payload: UserProfileUpdate): Promise<void> {
  const response = await apiClient.PATCH('/users/user/{user_id}', {
    params: {
      path: {
        user_id: userId,
      },
    },
    body: payload,
  });
  assertApiResponse(response, 'Nie udało się zaktualizować profilu.');
}

export async function changePassword(payload: PasswordChangePayload): Promise<void> {
  const response = await apiClient.POST('/users/me/password', {
    body: payload,
  });
  assertApiResponse(response, 'Nie udało się zmienić hasła.');
}

export async function anonymizeAccount(payload: AccountAnonymizePayload): Promise<void> {
  const response = await apiClient.POST('/users/me/anonymize', {
    body: payload,
  });
  assertApiResponse(response, 'Nie udało się zanonimizować konta.');
}
