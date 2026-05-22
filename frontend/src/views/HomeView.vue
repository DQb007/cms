<template>
  <div class="public-page">
    <main class="course-board">
      <header class="board-title">
        <h1>课程管理系统</h1>
      </header>

      <section class="search-console">
        <form class="filter-form" @submit.prevent="handleSearch">
          <div class="primary-search">
            <label class="field-control code-field">
              <span>课程编码</span>
              <input v-model.trim="query.code" type="search" placeholder="课程编码" />
            </label>
            <label class="field-control search-field">
              <span>课程名称</span>
              <input v-model.trim="query.name" type="search" placeholder="课程名称" />
            </label>
            <div class="field-control">
              <span>课程类型</span>
              <div class="custom-select" :class="{ open: categoryOpen }">
                <button type="button" class="custom-select__trigger" @click="toggleCategory">
                  <span>{{ selectedCategoryLabel }}</span>
                  <span class="custom-select__arrow" aria-hidden="true"></span>
                </button>
                <div v-if="categoryOpen" class="custom-select__menu">
                  <button
                    type="button"
                    class="custom-select__option"
                    :class="{ selected: query.category === '' }"
                    @click="selectCategory('')"
                  >
                    全部类型
                  </button>
                  <button
                    v-for="item in categories"
                    :key="item"
                    type="button"
                    class="custom-select__option"
                    :class="{ selected: query.category === item }"
                    @click="selectCategory(item)"
                  >
                    {{ item }}
                  </button>
                </div>
              </div>
            </div>
            <div class="field-control field-control--price">
              <span>课程价格</span>
              <div class="price-range">
                <input v-model.number="query.price_min" type="number" min="0" inputmode="numeric" placeholder="价格从" />
                <input v-model.number="query.price_max" type="number" min="0" inputmode="numeric" placeholder="价格到" />
              </div>
            </div>
          </div>

          <div class="filter-actions">
            <button class="primary-action" type="submit">查询</button>
            <button class="secondary-action" type="button" @click="handleReset">重置</button>
          </div>
        </form>
      </section>

      <section class="catalog-panel">
        <div class="public-table-wrap" :class="{ loading }">
          <table class="course-table public-table">
            <thead>
              <tr>
                <th class="select-col"><span class="fake-checkbox"></span></th>
                <th>课程编码</th>
                <th>课程类型</th>
                <th>课程名称</th>
                <th>课程链接</th>
                <th>价格</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="course in courses" :key="course.id">
                <td class="select-col"><span class="fake-checkbox"></span></td>
                <td><span class="code-badge">{{ course.code }}</span></td>
                <td>
                  <span v-if="course.category" class="type-pill">{{ course.category }}</span>
                  <span v-else class="muted-text">未分类</span>
                </td>
                <td>
                  <div class="course-name-cell">
                    <span class="course-dot"></span>
                    <span>{{ course.name }}</span>
                  </div>
                </td>
                <td>
                  <a v-if="course.url" :href="course.url" target="_blank" rel="noopener noreferrer" class="course-link">
                    课程简介
                  </a>
                  <span v-else class="muted-text">暂无链接</span>
                </td>
                <td>
                  <span class="price-token" :class="{ free: course.price === 0 }">
                    {{ course.price === 0 ? '免费' : course.price }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="!loading && courses.length === 0" class="empty-state">暂无课程数据</div>
          <div v-if="loading" class="loading-mask">加载中...</div>
        </div>

        <div class="mobile-course-list" :class="{ loading }">
          <article v-for="course in courses" :key="course.id" class="mobile-course-card">
            <div class="mobile-course-card__head">
              <span class="code-badge">{{ course.code }}</span>
              <span class="price-token" :class="{ free: course.price === 0 }">
                {{ course.price === 0 ? '免费' : course.price }}
              </span>
            </div>
            <h3>{{ course.name }}</h3>
            <div class="mobile-course-card__meta">
              <span v-if="course.category" class="type-pill">{{ course.category }}</span>
              <span v-else class="muted-text">未分类</span>
              <a v-if="course.url" :href="course.url" target="_blank" rel="noopener noreferrer" class="course-link">
                课程简介
              </a>
              <span v-else class="muted-text">暂无链接</span>
            </div>
          </article>
          <div v-if="!loading && courses.length === 0" class="empty-state">暂无课程数据</div>
          <div v-if="loading" class="loading-mask">加载中...</div>
        </div>

        <div class="pagination-bar public-pagination">
          <span class="total-text">共 {{ total }} 条</span>
          <div class="custom-select page-size-dropdown" :class="{ open: pageSizeOpen }">
            <button type="button" class="custom-select__trigger" @click="togglePageSize">
              <span>{{ query.page_size }}条/页</span>
              <span class="custom-select__arrow" aria-hidden="true"></span>
            </button>
            <div v-if="pageSizeOpen" class="custom-select__menu custom-select__menu--up">
              <button
                v-for="size in pageSizes"
                :key="size"
                type="button"
                class="custom-select__option"
                :class="{ selected: query.page_size === size }"
                @click="selectPageSize(size)"
              >
                {{ size }}条/页
              </button>
            </div>
          </div>
          <div class="pager-controls">
            <button type="button" :disabled="query.page <= 1" @click="goToPage(query.page - 1)">‹</button>
            <button
              v-for="item in pagerItems"
              :key="item.key"
              type="button"
              :class="{ active: item.page === query.page, ellipsis: item.ellipsis }"
              :disabled="item.ellipsis"
              @click="item.page && goToPage(item.page)"
            >
              {{ item.label }}
            </button>
            <button type="button" :disabled="query.page >= totalPages" @click="goToPage(query.page + 1)">›</button>
          </div>
          <label class="jump-control">
            前往
            <input v-model.number="jumpPage" type="number" min="1" :max="totalPages" @keyup.enter="confirmJump" />
            页
          </label>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'

import { getPublicCategories, getPublicCourses } from '@/api/public-courses'
import type { Course, CourseQuery } from '@/types/course'

const loading = ref(false)
const courses = ref<Course[]>([])
const total = ref(0)
const categories = ref<string[]>([])
const jumpPage = ref(1)
const categoryOpen = ref(false)
const pageSizeOpen = ref(false)
const pageSizes = [5, 10, 20, 50]

const query = reactive<CourseQuery>({
  code: '',
  name: '',
  category: '',
  price_min: null,
  price_max: null,
  page: 1,
  page_size: 5,
})

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / Number(query.page_size || 5))))
const selectedCategoryLabel = computed(() => query.category || '全部类型')

const pagerItems = computed(() => {
  const current = Number(query.page || 1)
  const last = totalPages.value
  const pages = new Set<number>([1, last])
  for (let page = current - 2; page <= current + 2; page += 1) {
    if (page >= 1 && page <= last) pages.add(page)
  }
  const sorted = Array.from(pages).sort((a, b) => a - b)
  const items: Array<{ key: string; label: string; page?: number; ellipsis?: boolean }> = []
  sorted.forEach((page, index) => {
    const previous = sorted[index - 1]
    if (previous && page - previous > 1) {
      items.push({ key: `ellipsis-${previous}-${page}`, label: '...', ellipsis: true })
    }
    items.push({ key: `page-${page}`, label: String(page), page })
  })
  return items
})

async function loadCourses() {
  loading.value = true
  try {
    const data = await getPublicCourses(query)
    courses.value = data.items
    total.value = data.total
    jumpPage.value = query.page || 1
  } finally {
    loading.value = false
  }
}

async function loadCategories() {
  const data = await getPublicCategories()
  categories.value = data.categories
}

function handleSearch() {
  query.page = 1
  loadCourses()
}

function handleReset() {
  query.code = ''
  query.name = ''
  query.category = ''
  query.price_min = null
  query.price_max = null
  query.page = 1
  query.page_size = 5
  loadCourses()
}

function toggleCategory() {
  categoryOpen.value = !categoryOpen.value
  pageSizeOpen.value = false
}

function selectCategory(value: string) {
  query.category = value
  categoryOpen.value = false
}

function togglePageSize() {
  pageSizeOpen.value = !pageSizeOpen.value
  categoryOpen.value = false
}

function selectPageSize(size: number) {
  query.page_size = size
  pageSizeOpen.value = false
  handlePageSizeChange()
}

function closeCategoryOnOutsideClick(event: MouseEvent) {
  const target = event.target as HTMLElement | null
  if (!target?.closest('.custom-select')) {
    categoryOpen.value = false
    pageSizeOpen.value = false
  }
}

function handlePageSizeChange() {
  query.page = 1
  loadCourses()
}

function goToPage(page: number) {
  const target = Math.min(Math.max(page, 1), totalPages.value)
  if (target === query.page) return
  query.page = target
  loadCourses()
}

function confirmJump() {
  goToPage(Number(jumpPage.value || 1))
}

onMounted(() => {
  document.addEventListener('click', closeCategoryOnOutsideClick)
  loadCategories()
  loadCourses()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', closeCategoryOnOutsideClick)
})
</script>
