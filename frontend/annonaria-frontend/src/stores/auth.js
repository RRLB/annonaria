// Pinia store for handling authentication state and token management.
// Stores the JWT token, provides an authentication status getter, and defines login/logout actions.

import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  // Initial state: retrieve token from localStorage if it exists
  state: () => ({
    token: localStorage.getItem('token') || null,
  }),

  // Getter: returns true if the user is authenticated (i.e., token exists)
  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  // Actions: login and logout update both state and localStorage
  actions: {
    login(token) {
      console.log('Logging in with token:', token);
      this.token = token;
      localStorage.setItem('token', token); // Persist token to localStorage
    },
    logout() {
      console.log('Logging out');
      this.token = null;
      localStorage.removeItem('token'); // Clear token from localStorage
    },
  }
});
