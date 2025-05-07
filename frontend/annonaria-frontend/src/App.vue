<!-- Root Vue component for the Annonaria frontend. -->
<!-- Defines the main layout with a responsive navigation bar and renders routed components. -->

<template>
  <div>
    <!-- Navigation bar using Bootstrap, re-renders when isAuthenticated changes -->
    <nav class="navbar navbar-expand-lg" :key="isAuthenticated">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Annonaria</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <!-- Left-aligned links -->
          <ul class="navbar-nav">
            <li class="nav-item" v-if="isAuthenticated">
              <router-link class="nav-link" to="/">Campaigns</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link class="nav-link" to="/create">Create Campaign</router-link>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a v-if="isAuthenticated" class="nav-link" href="#" @click.prevent="handleLogout">Logout</a>
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
import { computed, watch } from 'vue';
import { storeToRefs } from 'pinia'; 

// Initialize Pinia auth store and extract reactive isAuthenticated state
const authStore = useAuthStore();
const { isAuthenticated } = storeToRefs(authStore); // Use storeToRefs for reactivity
// Initialize Vue Router utilities
const route = useRoute();
const router = useRouter();

// Watch isAuthenticated for debugging and potential side effects
watch(isAuthenticated, (newValue) => {
  console.log('isAuthenticated changed:', newValue);
});

const isLoginPage = computed(() => route.path === '/login');
const isRegisterPage = computed(() => route.path === '/register');

// Handle logout by clearing auth state and redirecting to login page
function handleLogout() {
  authStore.logout();
  router.push('/login'); // Route change helps trigger reactive update
}
</script>
