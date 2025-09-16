<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import BaseInput from '../components/BaseInput.vue'
import BaseButton from '../components/BaseButton.vue'

const userStore = useUserStore()
const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const isLoading = ref(false)

async function handleRegister() {
  if (!username.value || !email.value || !password.value) {
    alert('请填写所有字段')
    return
  }
  isLoading.value = true
  try {
    const success = await userStore.register(
      username.value,
      email.value,
      password.value
    )
    if (success) {
      router.push({ name: 'dashboard' })
      // 因为 register action 内部已经调用了 login 并跳转，所以这里不需要再跳转
      // 如果你想让跳转逻辑更明确地在组件中，可以让 register action 只负责注册
      // 但目前的实现也可以工作
    }
  } catch (error) {
    // 這段代碼可以處理任何類型的錯誤，即使是網絡完全中斷
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
      <h1 class="text-3xl font-bold text-center text-gray-800">创建账户</h1>
      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">用户名</label>
          <BaseInput
            id="username"
            type="text"
            v-model="username"
            placeholder="你的昵称"
            class="mt-1"
          />
        </div>
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
            placeholder="至少6个字符"
            class="mt-1"
          />
        </div>
        <BaseButton type="submit" :disabled="isLoading">
          {{ isLoading ? '注册中...' : '注册' }}
        </BaseButton>
      </form>
      <p class="text-sm text-center text-gray-600">
        已经有账户了？
        <RouterLink to="/login" class="font-medium text-blue-600 hover:text-blue-500">
          直接登录
        </RouterLink>
      </p>
    </div>
  </div>
</template>