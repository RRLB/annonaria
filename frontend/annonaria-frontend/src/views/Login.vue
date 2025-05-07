<!-- Provides a user login form for the Annonaria frontend. -->
<!-- Sends credentials to the backend API, stores the access token on success, -->
<!-- handles login errors, and redirects to the home page upon successful authentication. -->

<template>
    <div class="row justify-content-center">
        <div class="col-md-6">
            <h1>Login</h1>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <form @submit.prevent="login">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input v-model="form.username" type="text" class="form-control" id="username" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input v-model="form.password" type="text" class="form-control" id="password" required>
                </div>
                <button type="submit" class="btn btn-primary">Login</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useAuthStore } from '../stores/auth'; 

export default {
    name: 'Login',
    data() {
        return {
            form: {
                username: '',
                password: ''
            },
            error: null
        };
    },
    methods: {
        async login() {
            const auth = useAuthStore(); // get store instance
            try {
                const response = await axios.post('http://localhost:4000/api/v1/login', this.form);
                const token = response.data.access_token;

                auth.login(token); // ✅ update store and localStorage

                this.$router.push('/');
            } catch (err) {
                if (err.response && err.response.status === 401) {
                    this.error = 'Invalid credentials';
                } else {
                    this.error = 'An error occurred. Please try again later.';
                }
            }
        }
    }
};
</script>