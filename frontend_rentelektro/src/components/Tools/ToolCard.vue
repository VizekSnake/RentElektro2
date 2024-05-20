<template>
  <v-card>
    <v-img :src="tool.ImageURL" height="200px"></v-img>
    <v-card-title>{{ tool.Type }}</v-card-title>
    <v-card-subtitle>{{ tool.Brand }}</v-card-subtitle>
    <v-card-text>
      <div>
        <strong>Category:</strong> {{ tool.CategoryID }}
      </div>
      <div>
        <strong>Rate Per Day:</strong> ${{ tool.RatePerDay }}
      </div>
    </v-card-text>
    <v-card-actions>
      <v-btn :to="{ name: 'ToolProfileView', params: { id: tool.id } }" text color="primary">
        Details
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'ToolCard',
  props: {
    tool: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
.v-card {
  margin-bottom: 20px;
}
</style>
