<template>
  <v-img :src="imageUrl" height="400px"></v-img>
</template>

<script>
export default {
  name: 'ToolImage',
  props: {
    imageUrl: {
      type: String,
      required: true
    }
  }
};
</script>
