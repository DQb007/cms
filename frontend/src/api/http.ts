import axios from 'axios'
import { ElMessage } from 'element-plus/es/components/message/index.mjs'

import { useAuthStore } from '@/stores/auth'

export const http = axios.create({
  baseURL: '/api',
  timeout: 12000,
})

http.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    if (error.response?.status === 401) {
      const auth = useAuthStore()
      auth.logout()
    }
    ElMessage.error(message)
    return Promise.reject(error)
  },
)
