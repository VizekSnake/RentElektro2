import apiClient from '@/shared/api/apiClient';
import { unwrapApiResponse } from '@/shared/api/apiErrors';
import type {
  PaginatedTools,
  Tool,
  ToolCategory,
  ToolFormPayload,
  ToolListFilters,
  ToolUpdatePayload,
} from '@/types/tools';

export async function fetchTools(filters: ToolListFilters = {}): Promise<PaginatedTools> {
  const response = await apiClient.GET('/tool/all', {
    params: {
      query: {
        search: filters.search,
        power_source: filters.power_source,
        availability: filters.availability,
        category_id: filters.category_id,
        sort: filters.sort ?? 'newest',
        page: filters.page ?? 1,
        page_size: filters.page_size ?? 9,
      },
    },
  });
  return unwrapApiResponse(response, 'Nie udało się pobrać listy narzędzi.');
}

export async function fetchToolById(id: string | number): Promise<Tool> {
  const response = await apiClient.GET('/tool/{tool_id}', {
    params: {
      path: {
        tool_id: Number(id),
      },
    },
  });
  return unwrapApiResponse(response, 'Nie udało się pobrać szczegółów narzędzia.');
}

export async function fetchToolCategories(): Promise<ToolCategory[]> {
  const response = await apiClient.GET('/tool/category/all');
  return unwrapApiResponse(response, 'Nie udało się pobrać kategorii narzędzi.') ?? [];
}

export async function fetchMyTools(): Promise<Tool[]> {
  const response = await apiClient.GET('/tool/mine');
  return unwrapApiResponse(response, 'Nie udało się pobrać Twoich narzędzi.');
}

export async function createTool(payload: ToolFormPayload): Promise<Tool> {
  if (payload.ImageURL.startsWith('data:')) {
    throw new Error('Do zapisu oferty podaj publiczny adres URL obrazka. Lokalny plik nie jest jeszcze wysyłany na serwer.');
  }

  const response = await apiClient.POST('/tool/add', { body: payload });
  return unwrapApiResponse(response, 'Nie udało się dodać narzędzia.');
}

export async function updateTool(toolId: number, payload: ToolUpdatePayload): Promise<Tool> {
  const response = await apiClient.PATCH('/tool/update/{tool_id}', {
    params: {
      path: {
        tool_id: toolId,
      },
    },
    body: payload,
  });
  return unwrapApiResponse(response, 'Nie udało się zaktualizować oferty.');
}
