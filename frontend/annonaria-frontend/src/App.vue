<template>
  <div>
    <nav class="navbar navbar-expand-lg">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Annonaria</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <!-- Left-aligned links -->
          <ul class="navbar-nav">
            <li class="nav-item" v-if="auth.isAuthenticated">
              <router-link class="nav-link" to="/">Campaigns</router-link>
            </li>
            <li class="nav-item" v-if="auth.isAuthenticated">
              <router-link class="nav-link" to="/create">Create Campaign</router-link>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a v-if="auth.isAuthenticated" class="nav-link" href="#" @click.prevent="handleLogout">Logout</a>
              <router-link v-else-if="isLoginPage" class="nav-link" to="/register">Register</router-link>
              <router-link v-else-if="isRegisterPage" class="nav-link" to="/login">Login</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth';
import { useRoute, useRouter } from 'vue-router';
import { computed } from 'vue';

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();

const isLoginPage = computed(() => route.path === '/login');
const isRegisterPage = computed(() => route.path === '/register');

function handleLogout() {
  auth.logout();
  router.push('/login'); // Route change helps trigger reactive update
}
</script>
