<template>
  <v-card>
    <v-card-title>{{ tool.Type }}</v-card-title>
    <v-card-subtitle>{{ tool.Brand }}</v-card-subtitle>
    <v-card-text>
      <div>
        <strong>Category:</strong> {{ tool.CategoryID }}
      </div>
      <div>
        <strong>Rate Per Day:</strong> ${{ tool.RatePerDay }}
      </div>
      <div>
        <strong>Description:</strong> {{ tool.Description }}
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'ToolDetails',
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
  margin-top: 20px;
}
</style>
