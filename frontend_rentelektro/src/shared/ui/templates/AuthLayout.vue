<template>
  <v-container class="py-8 py-md-12">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="5">
        <v-sheet
          class="pa-6 pa-md-8 rounded-xl app-auth-shell"
          color="surface"
          border="md"
          elevation="6"
        >
          <div class="d-flex flex-column align-center text-center mb-6 app-auth-head">
            <div class="app-eyebrow mb-4">RentElektro Access</div>
            <div class="app-logo-wrap mb-5">
              <LogoRentElektroSVG fillColor="none" />
            </div>
            <h1 class="text-h4 font-weight-bold text-high-emphasis">
              {{ title }}
            </h1>
            <p
              v-if="subtitle"
              class="text-body-1 text-medium-emphasis mt-3"
            >
              {{ subtitle }}
            </p>
          </div>

          <slot />
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import LogoRentElektroSVG from '@/shared/branding/LogoRentElektroSVG.vue';

defineProps<{
  title: string;
  subtitle?: string;
}>();
</script>
