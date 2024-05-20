<template>
  <div class="signup">
    <img alt="Vue logo" src="../assets/logo.png">
    <SignUpForm />
  </div>
</template>

<script>
// @ is an alias to /src
import SignUpForm from "@/components/Auth/SignUpForm.vue";

export default {
  name: 'LoginView',
  components: {
    SignUpForm
  }
}
</script>
q