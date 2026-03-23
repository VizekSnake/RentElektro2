import apiClient from '@/shared/api/apiClient';
import type { UserProfile, UserProfileUpdate } from '@/types/profile';

export async function fetchProfile(): Promise<UserProfile> {
  const response = await apiClient.get<UserProfile>('/users/me/data');
  return response.data;
}

export async function updateProfile(userId: number, payload: UserProfileUpdate): Promise<void> {
  await apiClient.patch(`/users/user/${userId}`, payload);
}
