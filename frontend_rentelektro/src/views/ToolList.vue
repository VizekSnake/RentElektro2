<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4" v-for="tool in tools" :key="tool.id">
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
            <v-btn text color="primary">Details</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ToolList',
  data() {
    return {
      tools: []
    };
  },
  created() {
    this.fetchTools();
  },
  methods: {
    async fetchTools() {
      try {
        const response = await axios.get('http://localhost:8000/api/tool/all');
        this.tools = response.data;
      } catch (error) {
        console.error('Error fetching tools:', error);
      }
    }
  }
};
</script>

<style scoped>
.v-card {
  margin-bottom: 20px;
}
</style>