<template>
  <AuthLayout
    title="Logowanie"
    subtitle="Zaloguj się, aby zarządzać profilem, dodawać narzędzia i obsługiwać wynajmy."
  >
    <LoginForm />
  </AuthLayout>
</template>

<script setup lang="ts">
import LoginForm from '@/features/auth/components/LoginForm.vue';
import AuthLayout from '@/shared/ui/templates/AuthLayout.vue';
</script>
