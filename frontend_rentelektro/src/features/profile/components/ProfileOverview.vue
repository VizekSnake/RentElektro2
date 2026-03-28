<template>
  <section class="app-profile-overview-card">
    <div class="app-profile-overview-grid">
      <div class="d-flex align-center ga-4">
        <v-avatar size="104" class="app-profile-avatar">
          <img v-if="user.profile_picture" :src="user.profile_picture" alt="profile" class="app-avatar-img">
          <span v-else class="text-h4 font-weight-bold">{{ initials }}</span>
        </v-avatar>

        <div class="d-flex flex-column ga-2">
          <div class="text-overline">Konto</div>
          <h2 class="text-h4 font-weight-bold mb-0">{{ fullName }}</h2>
          <div class="text-body-1 app-muted-copy">@{{ user.username }}</div>
          <div class="d-flex flex-wrap ga-2 mt-1">
            <v-chip color="primary" variant="tonal" size="small">
              {{ user.company ? 'Konto firmowe' : 'Konto prywatne' }}
            </v-chip>
            <v-chip :color="user.is_active ? 'success' : 'warning'" variant="tonal" size="small">
              {{ user.is_active ? 'Aktywne' : 'Nieaktywne' }}
            </v-chip>
          </div>
        </div>
      </div>

      <div class="app-profile-quick-stats">
        <div class="app-profile-stat">
          <span class="app-profile-stat-label">Email</span>
          <strong>{{ user.email }}</strong>
        </div>
        <div class="app-profile-stat">
          <span class="app-profile-stat-label">Telefon</span>
          <strong>{{ user.phone || 'Nie dodano' }}</strong>
        </div>
        <div class="app-profile-stat">
          <span class="app-profile-stat-label">Rola</span>
          <strong>{{ user.role || 'Użytkownik' }}</strong>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { UserProfile } from '@/types/profile';

const props = defineProps<{
  user: UserProfile;
}>();

const fullName = computed(() => {
  const value = `${props.user.firstname} ${props.user.lastname}`.trim();
  return value || props.user.username;
});

const initials = computed(() => {
  const source = fullName.value.split(' ').filter(Boolean).slice(0, 2);
  return source.map((item) => item[0]?.toUpperCase() ?? '').join('') || 'R';
});
</script>
