<template>
  <v-card>
    <v-card-text>
      <v-row>
        <v-col cols="12" md="4">
          <v-date-picker v-model="startDate" label="Start Date"></v-date-picker>
        </v-col>
        <v-col cols="12" md="4">
          <v-date-picker v-model="endDate" label="End Date"></v-date-picker>
        </v-col>
        <v-col cols="12" md="4">
          <div>
            <strong>Selected Start Date:</strong> {{ startDate || 'N/A' }}
          </div>
          <div>
            <strong>Selected End Date:</strong> {{ endDate || 'N/A' }}
          </div>
          <div class="mt-2">
            <strong>Number of Days:</strong> {{ numberOfDays }}
          </div>
          <div class="mt-2">
            <strong>Total Cost:</strong> ${{ totalCost || 0 }}
          </div>
          <v-btn class="mt-4" @click="rentTool" color="primary">Rent it!</v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'RentalCalculator',
  props: {
    ratePerDay: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      startDate: null,
      endDate: null,
      totalCost: null,
      numberOfDays: 0
    };
  },
  watch: {
    startDate: 'calculateTotal',
    endDate: 'calculateTotal'
  },
  methods: {
    calculateTotal() {
      if (this.startDate && this.endDate) {
        const start = new Date(this.startDate);
        const end = new Date(this.endDate);
        const diffTime = Math.abs(end - start);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
        this.numberOfDays = diffDays;
        this.totalCost = diffDays * this.ratePerDay;
      } else {
        this.numberOfDays = 0;
        this.totalCost = 0;
      }
    },
    rentTool() {
      // Implement the rental logic here
      alert('Tool rented successfully!');
    }
  }
};
</script>

<style scoped>
.v-card {
  margin-top: 20px;
}
</style>
