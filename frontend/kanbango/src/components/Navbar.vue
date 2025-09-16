<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'

const userStore = useUserStore()
const router = useRouter()

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class=" shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center space-x-8">
          <RouterLink to="/" class="flex-shrink-0 flex  items-center space-x-2">
            <span class="text-xl font-bold text-gray-800">  KanbanGo  </span>
          </RouterLink>
        </div>
        
        <div v-if="userStore.user" class="flex items-center space-x-4">
          <span class="text-sm text-gray-600">
            你好, {{ userStore.user.username || userStore.user.email }}
          </span>
          <button
            @click="handleLogout"
            class="px-3 py-2 text-sm font-medium text-white bg-red-500 rounded-md hover:bg-red-600"
          >
            登出
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>