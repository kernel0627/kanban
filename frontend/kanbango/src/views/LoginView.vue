<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import BaseInput from '../components/BaseInput.vue'
import BaseButton from '../components/BaseButton.vue'

const userStore = useUserStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const isLoading = ref(false)

async function handleLogin() {
  if (!email.value || !password.value) {
    alert('请输入邮箱和密码')
    return
  }
  isLoading.value = true
  try {
    const success = await userStore.login(email.value, password.value)
    if (success) {
      router.push('/')
    }
  } catch (error) {
    const message = error.response?.data?.msg || error.message || '發生未知錯誤，請檢查後端服務器。';
    alert('操作失敗: ' + message);
    console.error(error);
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-xl shadow-lg">
      <h1 class="text-3xl font-bold text-center text-gray-800">登录</h1>
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">邮箱地址</label>
          <BaseInput
            id="email"
            type="email"
            v-model="email"
            placeholder="you@example.com"
            class="mt-1"
          />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">密码</label>
          <BaseInput
            id="password"
            type="password"
            v-model="password"
            placeholder="请输入密码"
            class="mt-1"
          />
        </div>
        <BaseButton type="submit" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </BaseButton>
      </form>
      <p class="text-sm text-center text-gray-600">
        还没有账户？
        <RouterLink to="/register" class="font-medium text-blue-600 hover:text-blue-500">
          立即注册
        </RouterLink>
      </p>
    </div>
  </div>
</template>