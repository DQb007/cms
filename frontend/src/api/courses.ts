import { http } from '@/api/http'
import type { Course, CourseForm, CourseListResponse, CourseQuery } from '@/types/course'

function normalizeQuery(query: CourseQuery) {
  return Object.fromEntries(
    Object.entries(query).filter(([, value]) => value !== '' && value !== null && value !== undefined),
  )
}

export function getCoursesApi(query: CourseQuery) {
  return http.get<CourseListResponse>('/courses', { params: normalizeQuery(query) })
}

export function getCategoriesApi() {
  return http.get<{ categories: string[] }>('/courses/categories')
}

export function createCourseApi(payload: CourseForm) {
  return http.post<Course>('/courses', payload)
}

export function updateCourseApi(id: number, payload: CourseForm) {
  return http.put<Course>(`/courses/${id}`, payload)
}

export function deleteCourseApi(id: number) {
  return http.delete(`/courses/${id}`)
}

export function batchDeleteCoursesApi(ids: number[]) {
  return http.delete<{ deleted: number }>('/courses/batch', { data: { ids } })
}
