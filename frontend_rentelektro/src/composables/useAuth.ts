import { computed, ref } from 'vue';
import type { SignUpPayload, SessionUser } from '@/services/authService';
import {
  ensureAuthenticated,
  getSessionUser,
  loginWithPassword,
  logoutSession,
  registerUser,
} from '@/services/authService';

export function useAuth() {
  const sessionUser = ref<SessionUser | null>(null);
  const isSubmitting = ref(false);
  const isAuthenticated = computed(() => Boolean(sessionUser.value));

  const syncSessionState = async (): Promise<SessionUser | null> => {
    sessionUser.value = await getSessionUser();
    return sessionUser.value;
  };

  const login = async (username: string, password: string): Promise<void> => {
    isSubmitting.value = true;
    try {
      await loginWithPassword(username, password);
      await syncSessionState();
    } finally {
      isSubmitting.value = false;
    }
  };

  const signup = async (payload: SignUpPayload): Promise<void> => {
    isSubmitting.value = true;
    try {
      await registerUser(payload);
    } finally {
      isSubmitting.value = false;
    }
  };

  const logout = async (): Promise<void> => {
    isSubmitting.value = true;
    try {
      await logoutSession();
      sessionUser.value = null;
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    sessionUser,
    isAuthenticated,
    isSubmitting,
    ensureAuthenticated,
    syncSessionState,
    login,
    signup,
    logout,
  };
}
