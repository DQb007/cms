import { defineStore } from 'pinia'

import { getMeApi, loginApi } from '@/api/auth'

interface AuthState {
  token: string
  username: string
}

const TOKEN_KEY = 'cms_token'
const USERNAME_KEY = 'cms_username'

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem(TOKEN_KEY) || '',
    username: localStorage.getItem(USERNAME_KEY) || '',
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    async login(username: string, password: string) {
      const { data } = await loginApi(username, password)
      this.token = data.access_token
      this.username = data.username
      localStorage.setItem(TOKEN_KEY, this.token)
      localStorage.setItem(USERNAME_KEY, this.username)
    },
    async loadProfile() {
      const { data } = await getMeApi()
      this.username = data.username || ''
      localStorage.setItem(USERNAME_KEY, this.username)
    },
    logout() {
      this.token = ''
      this.username = ''
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USERNAME_KEY)
    },
  },
})
