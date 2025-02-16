import { createRouter, createWebHistory } from 'vue-router';
import LoginForm from '@/views/LoginView/LoginForm.vue';
import EmailInput from '@/views/LoginView/EmailInput.vue';
import PasswordCreation from '@/views/LoginView/PasswordCreation.vue';
import MainView from '@/views/MainView.vue';
import SettingsView from '@/views/SettingsView.vue';
import MeetingView from '@/views/MeetingView.vue';
import axios from 'axios';

// Function to check if the user is authenticated by validating the token
async function isAuthenticated(): Promise<boolean> {
  const accessToken = document.cookie.split('; ').find(row => row.startsWith('access_token='))?.split('=')[1];
  
  if (!accessToken) {
    return false;
  }

  try {
    const response = await axios.get('https://voiceflow.ru/api/validate-token', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    return response.status === 200;
  } catch (error) {
    console.error('Token validation failed:', error);
    return false;
  }
}

const routes = [
  {
    path: '/',
    name: 'MainView',
    component: MainView,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'LoginForm',
    component: LoginForm
  },
  {
    path: '/check',
    name: 'EmailInput',
    component: EmailInput
  },
  {
    path: '/register',
    name: 'PasswordCreation',
    component: PasswordCreation
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

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const authenticated = await isAuthenticated();
    if (!authenticated) {
      next({ name: 'EmailInput' });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
