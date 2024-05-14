<template>
  <div class="profile">
    <ProfileOverview :user="user" v-if="user" />
    <ProfileEdit :user="user" @update-profile="handleUpdateProfile" v-if="user" />
    <ProfileSettings v-if="user" />
  </div>
</template>

<script>
import axios from 'axios';
import ProfileOverview from './ProfileOverview.vue';
import ProfileEdit from './ProfileEdit.vue';
import ProfileSettings from './ProfileSettings.vue';

export default {
  name: 'BaseProfile',
  components: {
    ProfileOverview,
    ProfileEdit,
    ProfileSettings
  },
  data() {
    return {
      user: null,
      userId: null
    }
  },
  created() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      try {
        const response = await axios.get('http://localhost:8000/api/users/me');
        this.user = response.data;
        this.userId = this.user.id;
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async handleUpdateProfile(updatedUser) {
      try {
        const response = await axios.patch(`http://localhost:8000/api/users/${this.userId}`, updatedUser);
        this.user = { ...this.user, ...response.data };
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    }
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
