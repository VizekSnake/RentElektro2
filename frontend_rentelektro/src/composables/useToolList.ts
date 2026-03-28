import { ref } from 'vue';
import { fetchTools as fetchToolsRequest } from '@/services/toolService';
import type { PaginatedTools, Tool, ToolListFilters } from '@/types/tools';

export function useToolList() {
  const tools = ref<Tool[]>([]);
  const isLoading = ref(false);
  const errorMessage = ref('');
  const total = ref(0);
  const totalPages = ref(1);
  const page = ref(1);
  const pageSize = ref(9);

  const fetchTools = async (filters: ToolListFilters = {}): Promise<void> => {
    isLoading.value = true;
    errorMessage.value = '';

    try {
      const response: PaginatedTools = await fetchToolsRequest({
        ...filters,
        page: filters.page ?? page.value,
        page_size: filters.page_size ?? pageSize.value,
      });
      tools.value = response.items;
      total.value = response.total;
      totalPages.value = response.total_pages;
      page.value = response.page;
      pageSize.value = response.page_size;
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
    total,
    totalPages,
    page,
    pageSize,
    fetchTools,
  };
}
