// main.js or main.ts
import { createApp } from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify'; // Your Vuetify plugin setup
import router from './router'; // Your Vue Router setup

const app = createApp(App);
app.use(vuetify);
app.use(router);
app.mount('#app');
