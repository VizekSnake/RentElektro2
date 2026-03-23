<template>
  <v-alert
    v-if="message"
    :type="type"
    :icon="type === 'success' ? 'mdi-check-circle-outline' : 'mdi-alert-circle-outline'"
  >
    {{ message }}
    <ProgressBar
      v-if="showProgressBar"
      class="mt-3"
      :duration="duration"
    />
  </v-alert>
</template>

<script setup lang="ts">
import ProgressBar from '@/shared/ui/atoms/ProgressBar.vue';

type MessageType = 'success' | 'error';

withDefaults(defineProps<{
  message?: string;
  type?: MessageType;
  showProgressBar?: boolean;
  duration?: number;
}>(), {
  message: '',
  type: 'success',
  showProgressBar: false,
  duration: 3000,
});
</script>
