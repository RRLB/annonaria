// Entry point for the Annonaria frontend Vue.js application.
// Initializes the Vue app, sets up Pinia for state management, integrates Vue Router,
// and applies Bootstrap and custom CSS for styling.

import './assets/styles.css';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.mount('#app');
