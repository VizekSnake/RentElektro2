import type { AxiosError } from 'axios';
import apiClient from '@/shared/api/apiClient';
import { createLogger } from '@/shared/lib/logger';

const logger = createLogger('auth-service');

export type SessionUser = {
  id: number;
  username: string;
};

type LoginResult = {
  authenticated: boolean;
  token_type: string;
};

export type SignUpPayload = {
  username: string;
  email: string;
  phone: string;
  firstname: string;
  lastname: string;
  company: boolean;
  password: string;
};

type ApiError = {
  detail?: string;
};

export async function loginWithPassword(username: string, password: string): Promise<void> {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  logger.info('login_attempt', { username });

  await apiClient.post<LoginResult>('/users/token', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });

  logger.info('login_success', { username });
}

export async function getSessionUser(): Promise<SessionUser | null> {
  try {
    const response = await apiClient.get<SessionUser>('/users/me');
    return response.data;
  } catch {
    return null;
  }
}

export async function refreshToken(): Promise<boolean> {
  try {
    logger.info('refresh_token_attempt');
    await apiClient.post('/users/refresh', {});
    logger.info('refresh_token_success');
    return true;
  } catch {
    logger.warn('refresh_token_failed');
    return false;
  }
}

export async function ensureAuthenticated(): Promise<boolean> {
  const sessionUser = await getSessionUser();
  if (sessionUser) {
    logger.debug('session_active', { userId: sessionUser.id });
    return true;
  }

  const refreshed = await refreshToken();
  if (!refreshed) {
    return false;
  }

  return Boolean(await getSessionUser());
}

export async function logoutSession(): Promise<void> {
  try {
    await apiClient.post('/users/logout', {});
  } catch {
    logger.warn('logout_request_failed');
  }
  logger.info('logout_success');
}

export async function registerUser(payload: SignUpPayload): Promise<void> {
  try {
    await apiClient.post('/users/register', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    const axiosError = error as AxiosError<ApiError>;
    logger.warn('register_failed', { detail: axiosError.response?.data?.detail });
    throw error;
  }
}
