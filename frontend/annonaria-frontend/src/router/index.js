import { createRouter, createWebHistory } from 'vue-router';
import CampaignList from '../views/Home.vue';
import CampaignForm from '../views/CampaignForm.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';

const routes = [
  {
    path: '/',
    name: 'CampaignList',
    component: CampaignList,
    meta: { requiresAuth: true }
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
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Global navigation redirects to login if not authenticated
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');

  if (to.meta.requiresAuth && !isAuthenticated){
    next({ name: 'Login'});
  } else {
    next();
  }
})

export default router;
