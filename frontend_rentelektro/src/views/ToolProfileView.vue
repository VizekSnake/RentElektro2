<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <ToolImage :imageUrl="tool.ImageURL" />
      </v-col>
      <v-col cols="12" md="6">
        <ToolDetails :tool="tool" />
      </v-col>
    </v-row>
    <v-row class="mt-4">
      <v-col cols="12">
        <RentalCalculator :ratePerDay="tool.RatePerDay" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import ToolImage from "@/components/Tools/ToolImage.vue";
import ToolDetails from "@/components/Tools/ToolDetails.vue";
import RentalCalculator from "@/components/Tools/RentalCalculator.vue";

export default {
  name: 'ToolProfileView',
  components: {
    ToolImage,
    ToolDetails,
    RentalCalculator
  },
  data() {
    return {
      tool: {}
    };
  },
  created() {
    this.fetchToolDetails();
  },
  methods: {
    async fetchToolDetails() {
      const toolId = this.$route.params.id;
      try {
        const response = await axios.get(`api/tool/${toolId}`);
        this.tool = response.data;
      } catch (error) {
        console.error('Error fetching tool details:', error);
      }
    }
  }
};
</script>

<style scoped>
.v-container {
  margin-top: 20px;
}
</style>
