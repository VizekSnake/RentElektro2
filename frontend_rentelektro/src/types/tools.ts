export type Tool = {
  id: number;
  Type: string;
  TypeLabel?: string | null;
  PowerSource: string;
  PowerSourceLabel?: string | null;
  Brand: string;
  Description: string;
  category_id?: number | null;
  CategoryID?: number | null;
  Availability: boolean;
  Insurance: boolean;
  Power: number | null;
  Age: number | null;
  RatePerDay: number | null;
  ImageURL: string;
  owner_id?: number;
};

export type ToolCategory = {
  id: number;
  name: string;
  description: string;
  active: boolean;
  creator_id: number;
};

export type ToolListFilters = {
  search?: string;
  power_source?: string;
  availability?: boolean;
  category_id?: number;
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
  category_id: number | null;
  Availability: boolean;
  Insurance: boolean;
  Power: number | null;
  Age: number | null;
  RatePerDay: number | null;
  ImageURL: string;
};

export type ToolUpdatePayload = Partial<ToolFormPayload>;

export const getToolCategoryId = (tool: Partial<Tool>): number | null =>
  tool.category_id ?? tool.CategoryID ?? null;
