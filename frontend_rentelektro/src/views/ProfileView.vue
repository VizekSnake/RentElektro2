<!-- src/views/ProfileView.vue -->
<template>
  <div class="profile-view">
    <MainProfile />
  </div>
</template>

<script>
import MainProfile from '@/components/Profile/MainProfile.vue';

export default {
  name: 'ProfileView',
  components: {
    MainProfile
  }
}
</script>

<style scoped>
.profile-view {
  padding: 20px;
}
</style>
