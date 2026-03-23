<template>
  <AuthLayout
    title="Rejestracja"
    subtitle="Załóż konto w RentElektro i zacznij wynajmować lub udostępniać sprzęt."
  >
    <SignUpForm />
  </AuthLayout>
</template>

<script setup lang="ts">
import SignUpForm from "@/features/auth/components/SignUpForm.vue";
import AuthLayout from '@/shared/ui/templates/AuthLayout.vue';
</script>
