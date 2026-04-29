import type { UUID } from '@/types/identifiers';

export type Tool = {
  id: UUID;
  public_id: string;
  Type: string;
  TypeLabel?: string | null;
  PowerSource: string;
  PowerSourceLabel?: string | null;
  CategoryName?: string | null;
  Brand: string;
  Description: string;
  category_id?: UUID | null;
  CategoryID?: UUID | null;
  Availability: boolean;
  Insurance: boolean;
  Power: number | null;
  Age: number | null;
  RatePerDay: number | null;
  ImageURL: string;
  owner_id?: UUID;
};

export type ToolCategory = {
  id: UUID;
  name: string;
  description: string;
  active: boolean;
  creator_id: UUID;
};

export type ToolListFilters = {
  search?: string;
  power_source?: string;
  availability?: boolean;
  category_id?: UUID;
  sort?: 'newest' | 'price_asc' | 'price_desc' | 'name';
  page?: number;
  page_size?: number;
};

export type PaginatedTools = {
  items: Tool[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
};

export type ToolFormPayload = {
  Type: string;
  PowerSource: string;
  Brand: string;
  Description: string;
  category_id: UUID | null;
  Availability: boolean;
  Insurance: boolean;
  Power: number | null;
  Age: number | null;
  RatePerDay: number | null;
  ImageURL: string;
};

export type ToolUpdatePayload = Partial<ToolFormPayload>;

export const getToolCategoryId = (tool: Partial<Tool>): UUID | null =>
  tool.category_id ?? tool.CategoryID ?? null;
