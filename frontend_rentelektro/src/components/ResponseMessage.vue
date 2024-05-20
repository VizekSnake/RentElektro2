<template>
  <v-alert v-if="message" :class="messageClass">
    {{ message }}
    <v-progress-linear
      v-if="showProgressBar"
      :model-value="progress"
      height="5"
      color="success"
      striped
      rounded
    ></v-progress-linear>
  </v-alert>
</template>

<script>
export default {
  props: {
    message: {
      type: String,
      required: false,
      default: ''
    },
    type: {
      type: String,
      required: false,
      default: 'success' // 'success' or 'error'
    },
    showProgressBar: {
      type: Boolean,
      default: false
    },
    duration: {
      type: Number,
      default: 3000 // Default to 3 seconds if not provided
    }
  },
  data() {
    return {
      progress: 0
    };
  },
  mounted() {
    if (this.showProgressBar) {
      this.startProgress();
    }
  },
  methods: {
    startProgress() {
      const interval = 100; // Update every 100ms
      const increment = 100 / (this.duration / interval);

      const progressInterval = setInterval(() => {
        this.progress += increment;
        if (this.progress >= 100) {
          clearInterval(progressInterval);
          this.progress = 100;
        }
      }, interval);
    }
  },
  computed: {
    messageClass() {
      return this.type === 'success' ? 'success-message' : 'error-message';
    }
  }
};
</script>

<style scoped>
.success-message {
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #4CAF50;
  background-color: #dff0d8;
  color: #3c763d;
  border-radius: 5px;
  position: relative;
}

.error-message {
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #f44336;
  background-color: #f2dede;
  color: #a94442;
  border-radius: 5px;
  position: relative;
}
</style>
