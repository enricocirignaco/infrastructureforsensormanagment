import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      meta: { requiresAuth: false },
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/',
      meta: { requiresAuth: true },
      component: () => import('@/views/MainLayout.vue'),
      redirect: '/dashboard',
      children: [
        { path: 'dashboard', component: () => import('@/views/Dashboard.vue') },
        { path: 'settings', component: () => import('@/views/SettingsView.vue') },
        { path: 'projects', component: () => import('@/views/Project/ProjectsView.vue') },
        { path: 'project/:id', component: () => import('@/views/Project/ProjectView.vue')},
        { path: '/project/:id/edit', component: () => import('@/views/Project/EditProjectView.vue') },
        { path: 'project/new', component: () => import('@/views/Project/NewProjectView.vue') },
        { path: '/commercial-sensors', component: () => import('@/views/CommercialSensor/CommercialSensorsView.vue') },
        { path: '/commercial-sensor/:id', component: () => import('@/views/CommercialSensor/CommercialSensorView.vue') },
        { path: '/commercial-sensor/:id/edit', component: () => import('@/views/CommercialSensor/EditCommercialSensorView.vue') },
        { path: '/commercial-sensor/new', component: () => import('@/views/CommercialSensor/NewCommercialSensorView.vue') },
        { path: '/node-templates', component: () => import('@/views/NodeTemplate/NodeTemplatesView.vue') },
        { path: '/node-template/:id', component: () => import('@/views/NodeTemplate/NodeTemplateView.vue') },
        { path: '/node-template/:id/edit', component: () => import('@/views/NodeTemplate/EditNodeTemplateView.vue') },
        { path: '/node-template/new', component: () => import('@/views/NodeTemplate/NewNodeTemplateView.vue') },
      ],
    },
    // Redirect not registered routes to notfound page
    {
      path: '/notfound',
      name: 'NotFound',
      meta: { requiresAuth: false },
      component: () => import('../views/NotFound.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/notfound',
    },
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
