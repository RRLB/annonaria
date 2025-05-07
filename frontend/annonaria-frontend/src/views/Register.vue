<!-- Provides a user registration form for the Annonaria frontend. -->
<!-- Displays success or error messages, sends registration data to the backend API, -->
<!-- stores the access token on success, and redirects to the home page. -->

<template>
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h1>Register</h1>
        <div v-if="message" class="alert alert-success">{{ message }}</div>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <form @submit.prevent="register">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input v-model="form.username" type="text" class="form-control" id="username" required>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" id="password" required>
          </div>
          <button type="submit" class="btn btn-primary">Register</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useAuthStore } from '../stores/auth';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'Register',
    data() {
      return {
        form: {
          username: '',
          password: ''
        },
        message: null,
        error: null
      };
    },
    // Composition API setup for using store and router
    setup() {
      const auth = useAuthStore();
      const router = useRouter();
      return { auth, router };
    },
    methods: {
      // Method to handle registration logic
      async register() {
        try {
          const response = await axios.post('http://localhost:4000/api/v1/register', this.form);
          this.message = response.data.message;
          this.error = null;
          // Update auth store and localStorage via auth.login
          this.auth.login(response.data.access_token); // Update auth store
          this.router.push('/'); // Navigate to home
        } catch (err) {
          this.error = err.response?.data?.message || 'Registration failed. Please try again.';
        }
      }
    }
  };
  </script>
  