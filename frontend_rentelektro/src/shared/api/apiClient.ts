import createClient from 'openapi-fetch';
import type { paths } from '@/shared/api/schema';

const apiClient = createClient<paths>({
  baseUrl: '/api',
  credentials: 'include',
});

export default apiClient;
