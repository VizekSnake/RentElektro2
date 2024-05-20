<template>
  <form @submit.prevent="login">
    <div>
      <label for="username">Nazwa użytkownika:</label>
      <input type="text" id="username" v-model="username" required>
    </div>
    <div>
      <label for="password">Hasło:</label>
      <input type="password" id="password" v-model="password" required>
    </div>
    <button type="submit">Zaloguj</button>

    <router-link to="/signup">Nie masz konta? Zarejestruj się!</router-link>
  </form>

</template>

<script>
import axios from 'axios';
import { saveToken } from '@/services/authService';
import eventBus from '@/eventBus';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      const formData = new URLSearchParams();
      formData.append('username', this.username);
      formData.append('password', this.password);

      try {
        const response = await axios.post('http://localhost:8000/api/users/token', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded' // Set the content type header for form-encoded data
          },
          withCredentials: true // Important for handling cookies if you are using them
        });

        console.log('Logged in successfully!', response);

        // Check if response and response.data are defined
        if (response && response.data) {
          saveToken(response);
          saveToken(response);
          eventBus.emit('login'); // Emit login event
          // Redirect to the home page or dashboard
          this.$router.push('/home'); // Use Vue Router for navigation
        } else {
          throw new Error('Invalid response from server');
        }
      } catch (error) {
        console.error('Login error:', error);
        alert("Failed to log in: " + (error.response?.data?.detail || error.message));
      }
    }
  }
};
</script>

<style scoped>
/* Add styling for the login form */
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