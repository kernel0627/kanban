import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

axios.defaults.baseURL = '/api'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('authToken') || null)

  const isLoggedIn = computed(() => !!user.value)

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('authToken', newToken)
    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
  }

  function clearUser() {
    user.value = null
    token.value = null
    localStorage.removeItem('authToken')
    delete axios.defaults.headers.common['Authorization']
  }

  async function register(username, email, password) {
    try {
      await axios.post('/register', { username, email, password })

      const loginSuccess = await login(email, password)
      return loginSuccess
    } catch (err) {
      console.error('注册失败:', err.response?.data)
      throw err.response?.data
    }
  }

  async function login(email, password) {
    const param = new URLSearchParams()
    param.append('username', email)
    param.append('password', password)
    
    try {
      const response = await axios.post('/login', param)
      const accessToken = response.data.access_token;
      if (accessToken) {
        setToken(accessToken); 
        await fetchUser();     
        return true;           
      }
      return false; // 以防万一后端没有返回 token
    } catch (err) {
      console.error('登录失败:', err.response?.data)
      clearUser()
      throw err.response?.data
    }
  }

  function logout() {
    clearUser()
  }

  async function fetchUser() {
    if (!token.value) return
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    try {
      const response = await axios.get('/me')
      user.value = response.data
    } catch (error) {
      console.error('获取用户信息失败:', error.response?.data)
      clearUser()
    }
  }

  return {
    user,
    token,
    isLoggedIn,
    register,
    login,
    logout,
    fetchUser,
    setToken,
    clearUser,
  }
})