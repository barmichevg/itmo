import { createRouter, createWebHistory } from 'vue-router'
import LoginView from './views/LoginView.vue'
import MainView from './views/MainView.vue'
import { api } from './api'

export const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'login', component: LoginView, meta: { guestOnly: true } },
        { path: '/main', name: 'main', component: MainView, meta: { requiresAuth: true } }
    ]
})

router.beforeEach(async (to) => {
    if (to.meta.requiresAuth) {
        try {
            await api.me()
            return true
        } catch (e) {
            if (e?.status === 401) return { name: 'login' }
            return { name: 'login' }
        }
    }

    if (to.meta.guestOnly) {
        try {
            await api.me()
            return { name: 'main' }
        } catch {
            return true
        }
    }

    return true
})
