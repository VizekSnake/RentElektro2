import apiClient from '@/shared/api/apiClient';
import { unwrapApiResponse } from '@/shared/api/apiErrors';
import type { UUID } from '@/types/identifiers';
import type {
  PaginatedTools,
  Tool,
  ToolCategory,
  ToolFormPayload,
  ToolListFilters,
  ToolUpdatePayload,
} from '@/types/tools';

export async function fetchTools(filters: ToolListFilters = {}): Promise<PaginatedTools> {
  const response = await apiClient.GET('/tools', {
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

export async function fetchToolById(id: UUID): Promise<Tool> {
  const response = await apiClient.GET('/tools/{tool_id}', {
    params: {
      path: {
        tool_id: id,
      },
    },
  });
  return unwrapApiResponse(response, 'Nie udało się pobrać szczegółów narzędzia.');
}

export async function fetchToolCategories(): Promise<ToolCategory[]> {
  const response = await apiClient.GET('/tools/categories');
  return unwrapApiResponse(response, 'Nie udało się pobrać kategorii narzędzi.') ?? [];
}

export async function fetchMyTools(): Promise<Tool[]> {
  const response = await apiClient.GET('/tools/mine');
  return unwrapApiResponse(response, 'Nie udało się pobrać Twoich narzędzi.');
}

export async function createTool(payload: ToolFormPayload): Promise<Tool> {
  if (payload.ImageURL?.startsWith('data:')) {
    throw new Error('Do zapisu oferty podaj publiczny adres URL obrazka. Lokalny plik nie jest jeszcze wysyłany na serwer.');
  }

  const response = await apiClient.POST('/tools', { body: payload });
  return unwrapApiResponse(response, 'Nie udało się dodać narzędzia.');
}

export async function updateTool(toolId: UUID, payload: ToolUpdatePayload): Promise<Tool> {
  const response = await apiClient.PATCH('/tools/{tool_id}', {
    params: {
      path: {
        tool_id: toolId,
      },
    },
    body: payload,
  });
  return unwrapApiResponse(response, 'Nie udało się zaktualizować oferty.');
}
