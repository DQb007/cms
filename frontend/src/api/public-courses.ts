import type { Course, CourseListResponse, CourseQuery } from '@/types/course'

function buildQuery(params: CourseQuery) {
  const search = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== '' && value !== null && value !== undefined) {
      search.set(key, String(value))
    }
  })
  return search.toString()
}

async function requestJson<T>(path: string): Promise<T> {
  const response = await fetch(`/api${path}`)
  if (!response.ok) {
    throw new Error(`请求失败：${response.status}`)
  }
  return response.json() as Promise<T>
}

export function getPublicCourses(params: CourseQuery) {
  const query = buildQuery(params)
  return requestJson<CourseListResponse>(`/courses${query ? `?${query}` : ''}`)
}

export function getPublicCategories() {
  return requestJson<{ categories: string[] }>('/courses/categories')
}
