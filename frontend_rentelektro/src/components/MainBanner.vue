<template>
  <v-container class="banner elevation-10">
    <v-img :src="imageUrl" height="200px">
      <v-row class="fill-height" align="center" justify="center">
        <v-col class="text-center">
          <h1 class="banner-title">{{ title }}</h1>
          <p class="banner-subtitle">{{ subtitle }}</p>
        </v-col>
      </v-row>
    </v-img>
  </v-container>
</template>

<script>
export default {
  name: 'MainBanner',
  props: {
    imageUrl: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      required: false,
      default: ''
    }
  }
};
</script>

<style scoped>
.banner {
  background-color: #007bff;
  margin-bottom: 20px;
  border-radius: 10px;
}
.banner-title {
  color: white;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
}
.banner-subtitle {
  color: white;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
}
</style>