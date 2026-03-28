import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { ensureAuthenticated } from '@/services/authService';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/home',
  },
  {
    path: '/local_front',
    redirect: '/home',
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/AboutView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('@/views/SignUpView.vue'),
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/rentals',
    name: 'rentals',
    component: () => import('@/views/RentalsView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tool/add',
    name: 'tool-add',
    component: () => import('@/views/ToolAddView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/tools',
    name: 'tools',
    component: () => import('@/views/ToolList.vue'),
  },
  {
    path: '/tool/:id',
    name: 'ToolProfileView',
    component: () => import('@/views/ToolProfileView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  if (!requiresAuth) {
    return true;
  }

  if (await ensureAuthenticated()) {
    return true;
  }

  return '/login';
});

export default router;
