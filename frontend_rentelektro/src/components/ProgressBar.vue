<template>
  <div>
    <v-progress-linear
      :value="value"
      :buffer-value="bufferValue"
      color="success"
    ></v-progress-linear>
  </div>
</template>

<script>
export default {
  props: {
    duration: {
      type: Number,
      default: 3000 // Default to 3 seconds if not provided
    }
  },
  data() {
    return {
      value: 0,
      bufferValue: 0,
      interval: null,
    }
  },
  mounted() {
    this.startBuffer();
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
  methods: {
    startBuffer() {
      const increment = 100 / (this.duration / 100); // Increment based on duration

      this.interval = setInterval(() => {
        this.value += increment;
        this.bufferValue = this.value;

        if (this.value >= 100) {
          clearInterval(this.interval);
          this.$emit('progress-complete');
        }
      }, 100);
    },
  },
}
</script>
