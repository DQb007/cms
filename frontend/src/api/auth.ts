import { http } from '@/api/http'

export interface LoginResult {
  access_token: string
  token_type: string
  username: string
}

export interface UserProfile {
  id: number
  username: string | null
}

export function loginApi(username: string, password: string) {
  return http.post<LoginResult>('/auth/login', { username, password })
}

export function getMeApi() {
  return http.get<UserProfile>('/auth/me')
}

export function changePasswordApi(oldPassword: string, newPassword: string) {
  return http.put<{ message: string }>('/auth/password', {
    old_password: oldPassword,
    new_password: newPassword,
  })
}
