<template>
  <AuthLayout
    title="Reset hasła"
    subtitle="Podaj adres email przypisany do konta. Jeśli konto istnieje, backend wygeneruje link resetu."
  >
    <ForgotPasswordForm />
  </AuthLayout>
</template>

<script setup lang="ts">
import ForgotPasswordForm from '@/features/auth/components/ForgotPasswordForm.vue';
import AuthLayout from '@/shared/ui/templates/AuthLayout.vue';
</script>
