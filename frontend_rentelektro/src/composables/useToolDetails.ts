import { ref } from 'vue';
import type { UUID } from '@/types/identifiers';
import { fetchToolById } from '@/services/toolService';
import type { Tool } from '@/types/tools';

export function useToolDetails() {
  const tool = ref<Tool | null>(null);
  const isLoading = ref(false);
  const errorMessage = ref('');

  const fetchToolDetails = async (id: UUID): Promise<void> => {
    isLoading.value = true;
    errorMessage.value = '';

    try {
      tool.value = await fetchToolById(id);
    } catch {
      errorMessage.value = 'Nie udało się pobrać szczegółów narzędzia.';
    } finally {
      isLoading.value = false;
    }
  };

  return {
    tool,
    isLoading,
    errorMessage,
    fetchToolDetails,
  };
}
