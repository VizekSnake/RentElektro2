// // src/services/authService.js
// import axios from 'axios';
// import { ref } from 'vue';
//
// const isAuthenticated = ref(false);
//
// const authService = {
//   async login(username, password) {
//     const formData = new URLSearchParams();
//     formData.append('username', username);
//     formData.append('password', password);
//
//     try {
//       const response = await axios.post('http://localhost:8000/api/users/login', formData, {
//         headers: {
//           'Content-Type': 'application/x-www-form-urlencoded'
//         },
//         withCredentials: true
//       });
//       isAuthenticated.value = true;
//       return response.data;
//     } catch (error) {
//       isAuthenticated.value = false;
//       throw error;
//     }
//   },
//
//   async fetchCurrentUser() {
//
//       const response = await axios.get('http://localhost:8000/api/users/me', {
//         withCredentials: true
//       });
//       return response.data;
//
//   },
//
//   isAuthenticated
// };
//
// export default authService;
