import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView,
    },
    {
      path: '/pushkin/history',
      name: 'History',
      component: () => import('@/views/pushkin/HistoryView.vue'),
    },
    {
      path: '/pushkin/works',
      name: 'Works',
      component: () => import('@/views/pushkin/WorksView.vue'),
    },
    {
      path: '/news',
      name: 'News',
      component: () => import('@/views/NewsView.vue'),
    },
    {
      path: '/join/form',
      name: 'Form',
      component: () => import('@/views/join/FormView.vue'),
    },
    {
      path: '/mason/principles',
      name: 'Principles',
      component: () => import('@/views/mason/PrinciplesView.vue'),
    },
    {
      path: '/mason/symbols',
      name: 'Symbols',
      component: () => import('@/views/mason/SymbolsView.vue'),
    },
    {
      path: '/mason/truth',
      name: 'Truth',
      component: () => import('@/views/mason/TruthView.vue'),
    },
    {
      path: '/vlf',
      name: 'VLF',
      component: () => import('@/views/articles/VlfView.vue'),
    },
    {
      path: '/ovlr',
      name: 'OVLR',
      component: () => import('@/views/articles/OvlrView.vue'),
    },
    {
      path: '/article/:id',
      name: 'Article',
      component: () => import('@/views/articles/UniversalArticle.vue'),
    },
    {
      path: '/article/hello',
      name: 'Hello',
      component: () => import('@/views/articles/HelloView.vue'),
    },
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('@/views/AdminPlaceholder.vue'),
    },
  ],
})

export default router
