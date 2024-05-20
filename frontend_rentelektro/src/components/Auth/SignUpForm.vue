<template>
  <v-container class="ma-5">
    <ResponseMessage :message="successMessage" type="success" :showProgressBar="true" :duration="redirectDuration" v-if="successMessage" />
    <ResponseMessage :message="errorMessage" type="error" v-if="errorMessage" />
  </v-container>
  <form v-if="!registrationSuccessful" @submit.prevent="signup">
    <div>
      <label for="username">Nazwa użytkownika:</label>
      <input type="text" id="username" v-model="username" required>
    </div>
    <div>
      <label for="email">Adres email:</label>
      <input type="email" id="email" v-model="email" required>
    </div>
    <div>
      <label for="phone">Telefon:</label>
      <input type="text" id="phone" v-model="phone" required>
    </div>
    <div>
      <label for="firstname">Imię:</label>
      <input type="text" id="firstname" v-model="firstname" required>
    </div>
    <div>
      <label for="lastname">Nazwisko:</label>
      <input type="text" id="lastname" v-model="lastname" required>
    </div>
    <div>
      <label for="company">Czy użytkownik biznesowy?:</label>
      <input type="checkbox" id="company" v-model="company">
    </div>
    <div>
      <label for="password1">Hasło:</label>
      <input type="password" id="password1" v-model="password1" required>
    </div>
    <div>
      <label for="password2">Powtórz hasło:</label>
      <input type="password" id="password2" v-model="password2" required>
    </div>
     <button type="submit">Zarejestruj</button>
  </form>
</template>

<script>
import axios from 'axios';
import ResponseMessage from "@/components/ResponseMessage.vue";

export default {
  components: {
    ResponseMessage
  },
  data() {
    return {
      username: '',
      email: '',
      phone: '',
      firstname: '',
      lastname: '',
      company: false,
      password1: '',
      password2: '',
      successMessage: '',
      errorMessage: '',
      redirectDuration: 3000,
      registrationSuccessful: false
    };
  },
  methods: {
    async signup() {
      if (this.password1 !== this.password2) {
        this.errorMessage = "Hasła nie pasują do siebie";
        this.successMessage = '';
        this.scrollToMessage();
        return;
      }

      const formData = {
        username: this.username,
        email: this.email,
        phone: this.phone,
        firstname: this.firstname,
        lastname: this.lastname,
        company: this.company,
        password: this.password1,
      };

      try {
        const response = await axios.post('http://localhost:8000/api/users/register', formData, {
          headers: {
            'Content-Type': 'application/json'
          },
        });

        this.successMessage = 'Rejestracja zakończona sukcesem!';
        this.errorMessage = '';
        this.registrationSuccessful = true;
        console.log('Signed up successfully!', response);
        this.scrollToMessage();
        setTimeout(() => {
          window.location.href = '/login';
        }, this.redirectDuration);
      } catch (error) {
        if (error.response && error.response.data && error.response.data.detail) {
          this.errorMessage = 'Rejestracja nie powiodła się: ' + error.response.data.detail;
        } else {
          this.errorMessage = 'Rejestracja nie powiodła się: ' + error.message;
        }
        this.successMessage = '';
        console.error('Sign up error:', error);
        this.scrollToMessage();
      }
    },
    scrollToMessage() {
      this.$nextTick(() => {
        const container = this.$el.querySelector('.ma-5');
        if (container) {
          container.scrollIntoView({ behavior: 'smooth' });
        }
      });
    }
  }
};
</script>

<style scoped>
form {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
