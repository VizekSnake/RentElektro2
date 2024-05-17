import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import ProfileView from '../views/ProfileView.vue';
import SignUpView from '@/views/SignUpView.vue';
import ToolAddView from '@/views/ToolAddView.vue';
import ToolList from "@/views/ToolList.vue";
import { getToken, refreshToken } from '@/services/authService'; // Adjust the import path

const routes = [
    {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/tool/add',
    name: 'tool-add',
    component: ToolAddView,
    meta: { requiresAuth: true }
  },
  {
    path: '/tools',
    name: 'tools',
    component: ToolList
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const token = getToken();

  if (requiresAuth) {
    if (!token) {
      next('/login');
    } else {
      try {
        await refreshToken();
        next();
      } catch {
        next('/login');
      }
    }
  } else {
    next();
  }
});

export default router;