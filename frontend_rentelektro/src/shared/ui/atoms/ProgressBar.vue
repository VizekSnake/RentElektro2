<template>
  <div>
    <v-progress-linear
      :model-value="value"
      :buffer-value="bufferValue"
      color="success"
    />
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue';

const emit = defineEmits(['progress-complete']);

const props = withDefaults(defineProps<{
  duration?: number;
}>(), {
  duration: 3000,
});

const value = ref(0);
const bufferValue = ref(0);
let interval: number | undefined;

onMounted(() => {
  const increment = 100 / (props.duration / 100);

  interval = window.setInterval(() => {
    value.value += increment;
    bufferValue.value = value.value;

    if (value.value >= 100) {
      if (interval) {
        window.clearInterval(interval);
      }
      emit('progress-complete');
    }
  }, 100);
});

onBeforeUnmount(() => {
  if (interval) {
    window.clearInterval(interval);
  }
});
</script>
