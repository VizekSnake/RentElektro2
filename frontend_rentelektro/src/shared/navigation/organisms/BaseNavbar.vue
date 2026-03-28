<template>
  <v-app-bar app color="transparent" elevation="0" class="app-bar-frame">
    <div class="app-nav-shell d-flex align-center w-100">
      <v-toolbar-title class="app-nav-logo">
        <router-link to="/home">
          <LogoRentElektroSVG fillColor="black" />
        </router-link>
      </v-toolbar-title>
      <v-spacer />
      <div class="d-none d-md-flex align-center ga-2 app-nav-links">
        <AppButton variant="text" to="/home">Strona główna</AppButton>
        <AppButton variant="text" to="/about">O serwisie</AppButton>
        <AppButton variant="text" to="/tools">Narzędzia</AppButton>
        <AppButton v-if="!isAuthenticated" variant="text" to="/login">Logowanie</AppButton>
        <AppButton v-if="!isAuthenticated" color="secondary" to="/signup">Rejestracja</AppButton>
        <v-menu v-if="isAuthenticated" location="bottom end">
          <template #activator="{ props }">
            <v-btn v-bind="props" class="app-nav-notification-btn" variant="text" icon>
              <v-badge :content="notificationCount" :model-value="notificationCount > 0" color="primary">
                <v-icon>mdi-bell-outline</v-icon>
              </v-badge>
            </v-btn>
          </template>
          <v-card class="app-shell-card app-nav-notification-menu">
            <v-card-text class="d-flex flex-column ga-3">
              <div>
                <div class="text-overline mb-1">Powiadomienia</div>
                <div class="text-body-2 app-muted-copy">Nowe prośby i aktualne decyzje dotyczące wynajmów.</div>
              </div>
              <div class="app-nav-notification-item">
                <div class="font-weight-bold">Prośby do akceptacji</div>
                <div class="app-muted-copy">{{ ownerPendingCount }} nowych</div>
              </div>
              <div class="app-nav-notification-item">
                <div class="font-weight-bold">Aktualizacje moich wynajmów</div>
                <div class="app-muted-copy">{{ renterUpdateCount }} nieodczytanych</div>
              </div>
              <div class="d-flex flex-wrap ga-2">
                <AppButton color="primary" to="/rentals">Otwórz centrum wynajmów</AppButton>
                <AppButton
                  variant="outlined"
                  color="secondary"
                  :disabled="notificationCount === 0"
                  @click="markNotificationsAsRead"
                >
                  Oznacz odczytane
                </AppButton>
              </div>
            </v-card-text>
          </v-card>
        </v-menu>
        <AppButton v-if="isAuthenticated" variant="text" to="/rentals">Centrum wynajmów</AppButton>
        <AppButton v-if="isAuthenticated" color="secondary" to="/tool/add">Dodaj ofertę</AppButton>
        <AppButton v-if="isAuthenticated" variant="text" to="/profile">Profil</AppButton>
        <AppButton v-if="isAuthenticated" variant="text" @click="logout">Wyloguj</AppButton>
      </div>
      <div class="d-flex d-md-none">
        <v-menu location="bottom end">
          <template #activator="{ props }">
            <v-btn v-bind="props" icon="mdi-menu" variant="text" color="secondary" />
          </template>
          <v-card class="app-shell-card app-mobile-nav" min-width="240">
            <v-card-text class="d-flex flex-column ga-2">
              <AppButton variant="text" to="/home">Strona główna</AppButton>
              <AppButton variant="text" to="/about">O serwisie</AppButton>
              <AppButton variant="text" to="/tools">Narzędzia</AppButton>
              <AppButton v-if="!isAuthenticated" variant="text" to="/login">Logowanie</AppButton>
              <AppButton v-if="!isAuthenticated" color="primary" to="/signup">Rejestracja</AppButton>
              <div v-if="isAuthenticated" class="app-nav-notification-item">
                <div class="font-weight-bold">Powiadomienia</div>
                <div class="app-muted-copy">
                  {{ ownerPendingCount }} próśb do decyzji, {{ renterUpdateCount }} aktualizacji
                </div>
              </div>
              <AppButton v-if="isAuthenticated" color="secondary" to="/tool/add">Dodaj ofertę</AppButton>
              <AppButton v-if="isAuthenticated" variant="text" to="/rentals">Centrum wynajmów</AppButton>
              <AppButton v-if="isAuthenticated" variant="text" to="/profile">Profil</AppButton>
              <AppButton v-if="isAuthenticated" variant="text" @click="logout">Wyloguj</AppButton>
            </v-card-text>
          </v-card>
        </v-menu>
      </div>
    </div>
  </v-app-bar>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';
import { fetchMyRentalRequests, fetchOwnerRentalInbox, markRentalNotificationsRead } from '@/services/rentalService';
import LogoRentElektroSVG from '@/shared/branding/LogoRentElektroSVG.vue';
import AppButton from '@/shared/ui/atoms/AppButton.vue';
import eventBus from '@/eventBus';
import type { Rental } from '@/types/rentals';

const router = useRouter();
const { isAuthenticated, syncSessionState, logout: performLogout } = useAuth();
const ownerPendingCount = ref(0);
const renterUpdateCount = ref(0);
let notificationsInterval: number | undefined;

const pendingStatuses: Rental['status'][] = ['not_viewed', 'viewed'];
const unreadOwnerStatuses: Rental['status'][] = ['not_viewed'];

const notificationCount = computed(() => ownerPendingCount.value + renterUpdateCount.value);

const resetNotifications = (): void => {
  ownerPendingCount.value = 0;
  renterUpdateCount.value = 0;
};

const loadNotifications = async (): Promise<void> => {
  if (!isAuthenticated.value) {
    resetNotifications();
    return;
  }

  try {
    const [ownerInbox, myRequests] = await Promise.all([
      fetchOwnerRentalInbox(),
      fetchMyRentalRequests(),
    ]);

    ownerPendingCount.value = ownerInbox.filter((item) => unreadOwnerStatuses.includes(item.status)).length;
    renterUpdateCount.value = myRequests.filter(
      (item) => !pendingStatuses.includes(item.status) && item.renter_seen_at == null,
    ).length;
  } catch {
    resetNotifications();
  }
};

const markNotificationsAsRead = async (): Promise<void> => {
  if (!notificationCount.value) {
    return;
  }

  try {
    await markRentalNotificationsRead({ scope: 'all' });
    await loadNotifications();
  } catch {
    return;
  }
};

const startNotificationsPolling = (): void => {
  if (notificationsInterval) {
    window.clearInterval(notificationsInterval);
  }
  notificationsInterval = window.setInterval(() => {
    void loadNotifications();
  }, 60000);
};

const handleLogin = (): void => {
  void syncSessionState();
  void loadNotifications();
};

const handleLogout = (): void => {
  void syncSessionState();
  resetNotifications();
};

const logout = async (): Promise<void> => {
  await performLogout();
  resetNotifications();
  eventBus.emit('logout');
  await router.push('/login');
};

onMounted(() => {
  eventBus.on('login', handleLogin);
  eventBus.on('logout', handleLogout);
  void syncSessionState().then(() => {
    void loadNotifications();
  });
  startNotificationsPolling();
});

onBeforeUnmount(() => {
  eventBus.off('login', handleLogin);
  eventBus.off('logout', handleLogout);
  if (notificationsInterval) {
    window.clearInterval(notificationsInterval);
  }
});
</script>
