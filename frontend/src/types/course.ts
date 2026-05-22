export interface Course {
  id: number
  code: string
  name: string
  url: string | null
  price: number
  category: string | null
  create_time: string | null
  creator: string | null
  modify_time: string | null
  modifier: string | null
}

export interface CourseForm {
  code: string
  name: string
  url: string
  price: number
  category: string
}

export interface CourseQuery {
  code?: string
  name?: string
  category?: string
  price_min?: number | null
  price_max?: number | null
  page: number
  page_size: number
}

export interface CourseListResponse {
  items: Course[]
  total: number
  page: number
  page_size: number
}
