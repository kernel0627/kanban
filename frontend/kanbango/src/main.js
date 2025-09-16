// src/main.js

import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia' 
import App from './App.vue'
import router from './router' 
import { useUserStore } from './stores/userStore'

async function startApp() {
    const app = createApp(App)

    app.use(createPinia()) 
    const userStore = useUserStore()
    try {
        await userStore.fetchUser()
    } catch (err) {
        console.error('Failed to fetch user on app start: ', err)
    }
    app.use(router) 
    app.mount('#app')
}

startApp()