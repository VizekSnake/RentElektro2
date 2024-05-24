<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4" v-for="tool in tools" :key="tool.id">
        <ToolCard :tool="tool" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import ToolCard from "@/components/Tools/ToolCard.vue";

export default {
  name: 'ToolList',
  components: {
    ToolCard
  },
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
        const response = await axios.get('api/tool/all');
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
