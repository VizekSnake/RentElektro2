<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <ProfileOverview :user="user" v-if="user" />
      </v-col>
      <v-col cols="12">
        <ProfileEdit :user="user" @update-profile="handleUpdateProfile" v-if="user" />
      </v-col>
      <v-col cols="12">
        <ProfileSettings v-if="user" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import ProfileOverview from './ProfileOverview.vue';
import ProfileEdit from './ProfileEdit.vue';
import ProfileSettings from './ProfileSettings.vue';

export default {
  name: 'MainProfile',
  components: {
    ProfileOverview,
    ProfileEdit,
    ProfileSettings
  },
  data() {
    return {
      user: null,
      userId: null
    };
  },
  created() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost/api/users/me/data', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.user = response.data;
        this.userId = this.user.id;
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async handleUpdateProfile(updatedUser) {
      try {
        const token = localStorage.getItem('access_token');

        await axios.patch(`http://backend/api/users/user/${this.userId}`, updatedUser, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        // Fetch updated user data
        await this.fetchUserData();
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    }
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.fetchUserData();
    });
  },
  beforeRouteUpdate(to, from, next) {
    this.fetchUserData();
    next();
  }
}
</script>

<style scoped>
.profile {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>