import apiClient from '@/shared/api/apiClient';
import type { Rental, RentalCreatePayload } from '@/types/rentals';

type MeResponse = {
  id: number;
  username: string;
};

export async function getCurrentUserId(): Promise<number | null> {
  try {
    const response = await apiClient.get<MeResponse>('/users/me');
    return response.data.id;
  } catch {
    return null;
  }
}

export async function createRental(payload: RentalCreatePayload): Promise<Rental> {
  const response = await apiClient.post<Rental>('/rental/add', payload);
  return response.data;
}
