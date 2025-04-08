import { createRouter, createWebHistory } from 'vue-router'

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
      meta: { requiresAuth: false },
      component: () => import('@/views/MainLayout.vue'),
      children: [
        { path: 'home', component: () => import('@/views/HomeView.vue') },
        { path: 'about', component: () => import('@/views/AboutView.vue') },
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
  const isLoggedIn = false // TODO: <-- replace this with your real auth check

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
