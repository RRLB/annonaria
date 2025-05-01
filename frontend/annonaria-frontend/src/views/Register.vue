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
    methods: {
      async register() {
        try {
          const response = await axios.post('http://localhost:4000/api/v1/register', this.form);
          this.message = response.data.message;
          this.error = null;
          // auto login after registering
          localStorage.setItem('token', response.data.access_token);
          this.$router.push('/');
        } catch (err) {
          this.error = err.response?.data?.message || 'Registration failed';
        }
      }
    }
  };
  </script>
  