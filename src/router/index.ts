import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import SettingsView from '@/views/SettingsView.vue'
import MeetingView from '@/views/MeetingView.vue'

let isAuthenticated = false; // Переменная для хранения состояния аутентификации

const routes = [
  {
    path: '/',
    name: 'MainView',
    component: MainView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView
  },
  {
    path: '/settings',
    name: 'SettingsView',
    component: SettingsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/meeting/:id',
    name: 'MeetingView',
    component: MeetingView,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'LoginView' });
  } else {
    next();
  }
});

export function setAuthenticated(authenticated: boolean) {
  isAuthenticated = authenticated;
}

export default router
