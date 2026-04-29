import type { components, paths } from '@/shared/api/generated/schema';
import type { UUID } from '@/types/identifiers';

export type Tool = components['schemas']['Tool'];
export type ToolCategory = components['schemas']['Category'];
export type ToolListFilters = NonNullable<paths['/tools']['get']['parameters']['query']>;
export type PaginatedTools = components['schemas']['PaginatedTools'];
export type ToolFormPayload = components['schemas']['ToolAdd'];
export type ToolUpdatePayload = components['schemas']['ToolUpdate'];

export const getToolCategoryId = (tool: Partial<Tool>): UUID | null => tool.category_id ?? null;
