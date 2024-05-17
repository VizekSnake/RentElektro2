<!-- src/components/ProfileOverview.vue -->
<template>
  <v-container class="profile-overview" max-width="600px">
    <v-card>
      <v-card-title class="text-center">
        <h3>Profil użytkownika</h3>
      </v-card-title>
      <v-card-text>
        <v-row justify="center">
          <v-col cols="12" class="text-center">
<!--            <v-avatar size="100">-->
<!--              <img :src="user.profile_picture" alt="profile" />-->
<!--            </v-avatar>-->
            <v-avatar size="100" class="avatar">
              <img :src="user.profile_picture" alt="profile" class="avatar-img"/>
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

<script>
export default {
  name: 'ProfileOverview',
  props: {
    user: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.profile-overview {
  padding: 20px;
}
.avatar-img {
  width: 100%; /* Ensures the image takes the full width of the avatar */
  height: 100%; /* Ensures the image takes the full height of the avatar */
  object-fit: cover; /* Ensures the image covers the avatar area without stretching */
  border-radius: 50%; /* Makes the image circular */
}
</style>
