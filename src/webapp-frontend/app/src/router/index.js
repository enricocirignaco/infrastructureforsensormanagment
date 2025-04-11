import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      meta: { requiresAuth: false },
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/',
      meta: { requiresAuth: true },
      component: () => import('@/views/MainLayout.vue'),
      children: [
        { path: 'settings', component: () => import('@/views/SettingsView.vue') },
      ]
    },
    // Redirect not registered routes to notfound page
    {
      path: '/notfound',
      name: 'NotFound',
      meta: { requiresAuth: false },
      component: () => import('../views/NotFound.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/notfound'
    }
  ],
})

// Navigation guard to check authentication. Redirect to login if not authenticated
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
