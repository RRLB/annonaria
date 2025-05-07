// Vue Router configuration for the application.
// Defines public and protected routes, and uses a global navigation guard to restrict access based on authentication.

import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import CampaignList from '../views/Home.vue';
import CampaignForm from '../views/CampaignForm.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';

const routes = [
  {
    path: '/',
    name: 'CampaignList',
    component: CampaignList,
    meta: { requiresAuth: true } // Only accessible if authenticated
  },
  {
    path: '/create',
    name: 'CreateCampaign',
    component: CampaignForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/edit/:id',
    name: 'EditCampaign',
    component: CampaignForm,
    props: true, // Pass route params as props to the component
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login // Public route
  },
  {
    path: '/register',
    name: 'Register',
    component: Register // Public route
  }
];

const router = createRouter({
  history: createWebHistory(), // Use HTML5 history mode
  routes
})

// Global navigation redirects to login if not authenticated
router.beforeEach((to, from, next) => {
  const auth = useAuthStore(); // Access the auth store

  // If the route requires authentication and user is not authenticated, redirect to login
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next(); // Proceed as normal
  }
});

export default router;
