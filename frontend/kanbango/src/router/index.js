// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'dashboard',
            component: DashboardView,
            meta: { requiresAuth: true }
        },
        {
            path: '/boards/:id', 
            name: 'board',
            component: () => import('../views/BoardView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/boards/new', 
            name: 'create-board',
            component: () => import('../views/CreateBoardView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegisterView.vue')
        }
    ]
})

router.beforeEach((to,from ,next) => {
    const userStore = useUserStore()
    
    if (to.meta.requiresAuth && !userStore.isLoggedIn) {
        next({ name: 'login' })
    }else if ((to.name === 'login' || to.name === 'register') && userStore.isLoggedIn){
        next({ name: 'dashboard' })
    }
     else {
        next()
    }
})

export default router