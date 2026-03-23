import { computed, ref } from 'vue';
import type { AxiosError } from 'axios';
import { createTool, fetchToolCategories } from '@/services/toolService';
import type { ToolCategory, ToolFormPayload } from '@/types/tools';

type ApiError = {
  detail?: string;
};

export function useToolForm() {
  const categories = ref<ToolCategory[]>([]);
  const isLoadingCategories = ref(false);
  const isSubmitting = ref(false);
  const errorMessage = ref('');

  const categoryOptions = computed(() =>
    categories.value
      .filter((item) => item.active)
      .map((item) => ({
        title: item.name,
        value: item.id,
      })),
  );

  const categoryHint = computed(() =>
    categoryOptions.value.length > 0
      ? 'Wybierz kategorię z listy dostępnej w systemie.'
      : errorMessage.value || 'Brak aktywnych kategorii. Dodaj kategorię po stronie backendu.',
  );

  const fetchCategories = async (): Promise<void> => {
    isLoadingCategories.value = true;
    errorMessage.value = '';

    try {
      categories.value = await fetchToolCategories();
    } catch (error) {
      const axiosError = error as AxiosError<ApiError>;
      errorMessage.value = axiosError.response?.data?.detail ?? 'Nie udało się pobrać kategorii.';
    } finally {
      isLoadingCategories.value = false;
    }
  };

  const addTool = async (payload: ToolFormPayload): Promise<void> => {
    isSubmitting.value = true;
    errorMessage.value = '';

    try {
      await createTool(payload);
    } catch (error) {
      const axiosError = error as AxiosError<ApiError>;
      errorMessage.value = axiosError.response?.data?.detail ?? 'Nie udało się dodać narzędzia.';
      throw error;
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    categories,
    categoryOptions,
    categoryHint,
    isLoadingCategories,
    isSubmitting,
    errorMessage,
    fetchCategories,
    addTool,
  };
}
