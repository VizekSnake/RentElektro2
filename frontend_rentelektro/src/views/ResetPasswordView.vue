<template>
  <AuthLayout
    title="Ustaw nowe hasło"
    subtitle="Wprowadź nowe hasło dla swojego konta RentElektro."
  >
    <ResetPasswordForm />
  </AuthLayout>
</template>

<script setup lang="ts">
import ResetPasswordForm from '@/features/auth/components/ResetPasswordForm.vue';
import AuthLayout from '@/shared/ui/templates/AuthLayout.vue';
</script>
