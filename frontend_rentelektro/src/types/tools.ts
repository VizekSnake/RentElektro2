export type Tool = {
  id: number;
  Type: string;
  PowerSource: string;
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

export const getToolCategoryId = (tool: Partial<Tool>): number | null =>
  tool.category_id ?? tool.CategoryID ?? null;
