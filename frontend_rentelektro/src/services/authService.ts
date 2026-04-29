import apiClient from '@/shared/api/apiClient';
import { assertApiResponse, unwrapApiResponse } from '@/shared/api/apiErrors';
import type { components } from '@/shared/api/generated/schema';
import { createLogger } from '@/shared/lib/logger';

const logger = createLogger('auth-service');

export type SessionUser = components['schemas']['SessionUser'];
export type SignUpPayload = components['schemas']['UserCreate'];
export type PasswordResetRequestPayload = components['schemas']['PasswordResetRequest'];
export type PasswordResetConfirmPayload = components['schemas']['PasswordResetConfirmRequest'];
export type MessageResponse = components['schemas']['MessageResponse'];

export async function loginWithPassword(username: string, password: string): Promise<void> {
  logger.info('login_attempt', { username });

  const response = await apiClient.POST('/users/token', {
    body: {
      scope: '',
      username,
      password,
    },
    bodySerializer(body) {
      const formData = new URLSearchParams();
      formData.append('username', body.username);
      formData.append('password', body.password);
      formData.append('scope', body.scope);
      return formData;
    },
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  unwrapApiResponse(response, 'Logowanie nie powiodło się.');

  logger.info('login_success', { username });
}

export async function getSessionUser(): Promise<SessionUser | null> {
  try {
    const response = await apiClient.GET('/users/me');
    return unwrapApiResponse(response, 'Nie udało się pobrać sesji użytkownika.');
  } catch {
    return null;
  }
}

export async function refreshToken(): Promise<boolean> {
  try {
    logger.info('refresh_token_attempt');
    const response = await apiClient.POST('/users/refresh', {});
    unwrapApiResponse(response, 'Odświeżenie sesji nie powiodło się.');
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
    const response = await apiClient.POST('/users/logout', {});
    assertApiResponse(response, 'Wylogowanie nie powiodło się.');
  } catch {
    logger.warn('logout_request_failed');
  }
  logger.info('logout_success');
}

export async function registerUser(payload: SignUpPayload): Promise<void> {
  try {
    const response = await apiClient.POST('/users', { body: payload });
    assertApiResponse(response, 'Rejestracja nie powiodła się.');
  } catch (error) {
    logger.warn('register_failed', { detail: error instanceof Error ? error.message : undefined });
    throw error;
  }
}

export async function requestPasswordReset(
  payload: PasswordResetRequestPayload,
): Promise<MessageResponse> {
  logger.info('password_reset_request_attempt', { email: payload.email });
  const response = await apiClient.POST('/users/password-reset/request', { body: payload });
  return unwrapApiResponse(response, 'Nie udało się wygenerować linku resetu hasła.');
}

export async function confirmPasswordReset(
  payload: PasswordResetConfirmPayload,
): Promise<MessageResponse> {
  logger.info('password_reset_confirm_attempt');
  const response = await apiClient.POST('/users/password-reset/confirm', { body: payload });
  return unwrapApiResponse(response, 'Nie udało się zresetować hasła.');
}
