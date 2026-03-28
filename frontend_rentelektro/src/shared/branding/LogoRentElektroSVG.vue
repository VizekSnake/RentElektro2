<script setup lang="ts">
import { computed } from 'vue';

type FillColor = 'black' | 'white' | 'none';

const props = withDefaults(defineProps<{
  fillColor?: FillColor;
}>(), {
  fillColor: 'black',
});

const logoClass = computed(() => `app-wordmark is-${props.fillColor}`);
</script>

<template>
  <div :class="logoClass">
    <div class="app-wordmark-main">
      <span class="app-wordmark-rent">Rent</span>
      <span class="app-wordmark-elektro">Elektro</span>
    </div>
    <div class="app-wordmark-tag">tool rental platform</div>
  </div>
</template>

<style scoped>
.app-wordmark {
  display: inline-flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.15rem;
  cursor: pointer;
  line-height: 1;
}

.app-wordmark-main {
  display: inline-flex;
  align-items: baseline;
  gap: 0.1rem;
  font-family: var(--app-display-font-family);
  font-size: clamp(1.5rem, 2vw, 2rem);
  font-weight: 800;
  letter-spacing: -0.07em;
}

.app-wordmark-tag {
  padding-left: 0.1rem;
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  opacity: 0.72;
}

.app-wordmark.is-black {
  color: #171717;
}

.app-wordmark.is-black .app-wordmark-elektro {
  color: var(--app-color-primary);
}

.app-wordmark.is-white {
  color: #ffffff;
}

.app-wordmark.is-white .app-wordmark-elektro {
  color: #ffd7b5;
}

.app-wordmark.is-none {
  color: var(--app-color-secondary);
}

.app-wordmark.is-none .app-wordmark-elektro {
  color: var(--app-color-primary);
}
</style>
