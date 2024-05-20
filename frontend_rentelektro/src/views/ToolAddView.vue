<template>
  <v-container>
    <v-card>
      <v-card-title>
        <h3>Add New Tool</h3>
      </v-card-title>
      <v-card-text>
        <ToolAddForm @tool-added="handleToolAdded" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import ToolAddForm from '@/components/Tools/ToolAddForm.vue';  // Adjust the path as necessary

export default {
  name: 'ToolAddView',
  components: {
    ToolAddForm,
  },
  methods: {
    handleToolAdded() {
      // Handle the event when a tool is successfully added
      this.$router.push('/tools');  // Redirect to the tools list page or any other page
    },
  },
};
</script>

<style scoped>
</style>
