import apiClient from '@/shared/api/apiClient';
import type { Tool, ToolCategory, ToolFormPayload } from '@/types/tools';

export async function fetchTools(): Promise<Tool[]> {
  const response = await apiClient.get<Tool[]>('/tool/all');
  return response.data;
}

export async function fetchToolById(id: string | number): Promise<Tool> {
  const response = await apiClient.get<Tool>(`/tool/${id}`);
  return response.data;
}

export async function fetchToolCategories(): Promise<ToolCategory[]> {
  const response = await apiClient.get<ToolCategory[]>('/tool/category/all');
  return response.data;
}

export async function createTool(payload: ToolFormPayload): Promise<void> {
  await apiClient.post('/tool/add', payload, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
