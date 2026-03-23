import { ref } from 'vue';
import { fetchTools as fetchToolsRequest } from '@/services/toolService';
import type { Tool } from '@/types/tools';

export function useToolList() {
  const tools = ref<Tool[]>([]);
  const isLoading = ref(false);
  const errorMessage = ref('');

  const fetchTools = async (): Promise<void> => {
    isLoading.value = true;
    errorMessage.value = '';

    try {
      tools.value = await fetchToolsRequest();
    } catch {
      errorMessage.value = 'Nie udało się pobrać listy narzędzi.';
    } finally {
      isLoading.value = false;
    }
  };

  return {
    tools,
    isLoading,
    errorMessage,
    fetchTools,
  };
}
