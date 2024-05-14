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
  </form>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      // Create URLSearchParams to send data as form-encoded
      const formData = new URLSearchParams();
      formData.append('username', this.username);
      formData.append('password', this.password);

      try {
        const response = await axios.post('http://localhost:8000/api/users/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded' // Set the content type header for form-encoded data
          },
          withCredentials: true  // Important for handling cookies if you are using them
        });
        console.log('Logged in successfully!', response);
        // Redirect or perform further actions post-login
        window.location.href = '/home'; // Redirect to a home page or dashboard
      } catch (error) {
        console.error('Login error:', error.response.data);
        alert("Failed to log in: " + error.response.data.detail);
      }
    }
  }
};
</script>
<!--<script>-->
<!--import axios from 'axios';-->

<!--export default {-->
<!--  data() {-->
<!--    return {-->
<!--      username: '',-->
<!--      password: ''-->
<!--    };-->
<!--  },-->
<!--  methods: {-->
<!--    async login() {-->
<!--      try {-->
<!--        const response = await axios.post('http://0.0.0.0:8000/api/users/login', {-->
<!--          username: this.username,-->
<!--          password: this.password-->
<!--        });-->
<!--        // Obsługa odpowiedzi - np. przekierowanie na inną stronę po zalogowaniu-->
<!--        console.log('Zalogowano pomyślnie!', response.data);-->
<!--      } catch (error) {-->
<!--        console.error('Błąd logowania:', error);-->
<!--        // Obsługa błędów - np. wyświetlenie komunikatu dla użytkownika-->
<!--      }-->
<!--    }-->
<!--  }-->
<!--};-->
<!--</script>-->

<style scoped>
/* Dodaj stylizację dla formularza logowania */
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
