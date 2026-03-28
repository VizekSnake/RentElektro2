import apiClient from '@/shared/api/apiClient';
import { unwrapApiResponse } from '@/shared/api/apiErrors';
import type {
  Rental,
  RentalCreatePayload,
  RentalDecisionPayload,
  RentalInboxItem,
  RentalNotificationsReadPayload,
  RentalNotificationsReadResult,
  RentalOwnerStatusPayload,
  RentalPaymentPayload,
} from '@/types/rentals';

export async function getCurrentUserId(): Promise<number | null> {
  try {
    const response = await apiClient.GET('/users/me');
    return unwrapApiResponse(response, 'Nie udało się pobrać bieżącego użytkownika.').id;
  } catch {
    return null;
  }
}

export async function createRental(payload: RentalCreatePayload): Promise<Rental> {
  const response = await apiClient.POST('/rental/add', { body: payload });
  return unwrapApiResponse(response, 'Nie udało się utworzyć wynajmu.');
}

export async function fetchOwnerRentalInbox(): Promise<RentalInboxItem[]> {
  const response = await apiClient.GET('/rental/inbox');
  return unwrapApiResponse(response, 'Nie udało się pobrać skrzynki wynajmów.');
}

export async function fetchMyRentalRequests(): Promise<RentalInboxItem[]> {
  const response = await apiClient.GET('/rental/my');
  return unwrapApiResponse(response, 'Nie udało się pobrać Twoich próśb o wynajem.');
}

export async function decideRental(
  rentalId: number,
  payload: RentalDecisionPayload,
): Promise<Rental> {
  const response = await apiClient.PATCH('/rental/{rental_id}/decision', {
    params: {
      path: {
        rental_id: rentalId,
      },
    },
    body: payload,
  });
  return unwrapApiResponse(response, 'Nie udało się zaktualizować decyzji właściciela.');
}

export async function payRental(
  rentalId: number,
  payload: RentalPaymentPayload,
): Promise<Rental> {
  const response = await apiClient.PATCH('/rental/{rental_id}/pay', {
    params: {
      path: {
        rental_id: rentalId,
      },
    },
    body: payload,
  });
  return unwrapApiResponse(response, 'Nie udało się opłacić wynajmu.');
}

export async function updateOwnerRentalStatus(
  rentalId: number,
  payload: RentalOwnerStatusPayload,
): Promise<Rental> {
  const response = await apiClient.PATCH('/rental/{rental_id}/owner-status', {
    params: {
      path: {
        rental_id: rentalId,
      },
    },
    body: payload,
  });
  return unwrapApiResponse(response, 'Nie udało się zaktualizować statusu wynajmu.');
}

export async function markRentalNotificationsRead(
  payload: RentalNotificationsReadPayload,
): Promise<RentalNotificationsReadResult> {
  const response = await apiClient.PATCH('/rental/notifications/read', {
    body: payload,
  });
  return unwrapApiResponse(response, 'Nie udało się oznaczyć powiadomień jako odczytane.');
}
