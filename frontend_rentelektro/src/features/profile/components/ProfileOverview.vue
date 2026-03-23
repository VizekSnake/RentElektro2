<template>
  <v-container class="app-profile-overview" max-width="600px">
    <v-card>
      <v-card-title class="text-center">
        <h3>Profil użytkownika</h3>
      </v-card-title>
      <v-card-text>
        <v-row justify="center">
          <v-col cols="12" class="text-center">
            <v-avatar size="100" class="avatar">
              <img :src="user.profile_picture" alt="profile" class="app-avatar-img">
            </v-avatar>
          </v-col>
          <v-col cols="12" class="text-center">
            <h2>{{ user.username }}</h2>
          </v-col>
          <v-col cols="12">
            <v-list>
              <v-list-item>
                <v-list-item-title>Email</v-list-item-title>
                <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import type { UserProfile } from '@/types/profile';

defineProps<{
  user: UserProfile;
}>();
</script>
