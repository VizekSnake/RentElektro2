import { ref } from 'vue';

import {
  decideRental,
  fetchMyRentalRequests,
  fetchOwnerRentalInbox,
  payRental,
  updateOwnerRentalStatus,
} from '@/services/rentalService';
import { fetchMyTools } from '@/services/toolService';
import type {
  RentalDecisionPayload,
  RentalInboxItem,
  RentalOwnerStatusPayload,
  RentalPaymentPayload,
} from '@/types/rentals';
import type { Tool } from '@/types/tools';

export function useRentalInbox() {
  const ownerInboxItems = ref<RentalInboxItem[]>([]);
  const myRequestItems = ref<RentalInboxItem[]>([]);
  const myTools = ref<Tool[]>([]);
  const isLoading = ref(false);
  const isSubmitting = ref(false);
  const errorMessage = ref('');
  const successMessage = ref('');

  const loadInbox = async (): Promise<void> => {
    isLoading.value = true;
    errorMessage.value = '';

    try {
      const [ownerInbox, myRequests, ownedTools] = await Promise.all([
        fetchOwnerRentalInbox(),
        fetchMyRentalRequests(),
        fetchMyTools(),
      ]);
      ownerInboxItems.value = ownerInbox;
      myRequestItems.value = myRequests;
      myTools.value = ownedTools;
    } catch {
      errorMessage.value = 'Nie udało się pobrać centrum wynajmów.';
    } finally {
      isLoading.value = false;
    }
  };

  const updateDecision = async (
    rentalId: number,
    payload: RentalDecisionPayload,
  ): Promise<void> => {
    isSubmitting.value = true;
    errorMessage.value = '';
    successMessage.value = '';

    try {
      await decideRental(rentalId, payload);
      successMessage.value =
        payload.status === 'accepted'
          ? 'Prośba została zaakceptowana.'
          : 'Prośba została odrzucona.';
      await loadInbox();
    } catch {
      errorMessage.value = 'Nie udało się zapisać decyzji właściciela.';
    } finally {
      isSubmitting.value = false;
    }
  };

  const submitPayment = async (
    rentalId: number,
    payload: RentalPaymentPayload,
  ): Promise<void> => {
    isSubmitting.value = true;
    errorMessage.value = '';
    successMessage.value = '';

    try {
      await payRental(rentalId, payload);
      successMessage.value = 'Płatność została zapisana.';
      await loadInbox();
    } catch {
      errorMessage.value = 'Nie udało się zapisać płatności.';
    } finally {
      isSubmitting.value = false;
    }
  };

  const advanceOwnerRentalStatus = async (
    rentalId: number,
    payload: RentalOwnerStatusPayload,
  ): Promise<void> => {
    isSubmitting.value = true;
    errorMessage.value = '';
    successMessage.value = '';

    try {
      await updateOwnerRentalStatus(rentalId, payload);
      successMessage.value =
        payload.status === 'paid_rented'
          ? 'Wynajem został oznaczony jako odebrany.'
          : 'Zwrot został potwierdzony.';
      await loadInbox();
    } catch {
      errorMessage.value = 'Nie udało się zaktualizować bieżącego wynajmu.';
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    ownerInboxItems,
    myRequestItems,
    myTools,
    isLoading,
    isSubmitting,
    errorMessage,
    successMessage,
    loadInbox,
    updateDecision,
    submitPayment,
    advanceOwnerRentalStatus,
  };
}
