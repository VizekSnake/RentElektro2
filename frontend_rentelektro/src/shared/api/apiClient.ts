import createClient from 'openapi-fetch';
import type { paths } from '@/shared/api/generated/schema';

const apiClient = createClient<paths>({
  baseUrl: '/api/v1',
  credentials: 'include',
});

export default apiClient;
