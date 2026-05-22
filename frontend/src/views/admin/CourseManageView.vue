<template>
  <div class="manage-view">
    <section class="admin-card">
      <el-form :model="query" label-width="76px" class="admin-filter">
        <div class="admin-filter-grid">
          <div class="admin-filter-field">
            <el-form-item label="课程编码">
              <el-input v-model="query.code" clearable placeholder="课程编码" />
            </el-form-item>
          </div>
          <div class="admin-filter-field">
            <el-form-item label="课程名称">
              <el-input v-model="query.name" clearable placeholder="课程名称" />
            </el-form-item>
          </div>
          <div class="admin-filter-field">
            <el-form-item label="课程类型">
              <el-select v-model="query.category" clearable filterable placeholder="请选择">
                <el-option v-for="item in categories" :key="item" :label="item" :value="item" />
              </el-select>
            </el-form-item>
          </div>
          <div class="admin-filter-field admin-filter-field--price">
            <el-form-item label="课程价格">
              <div class="price-range">
                <el-input-number v-model="query.price_min" :min="0" controls-position="right" placeholder="价格从" />
                <el-input-number v-model="query.price_max" :min="0" controls-position="right" placeholder="价格到" />
              </div>
            </el-form-item>
          </div>
          <div class="admin-filter-field admin-filter-field--actions">
            <div class="admin-filter-actions admin-filter-actions--stacked">
              <div class="admin-filter-actions__bottom">
                <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
                <el-button :icon="RefreshRight" @click="handleReset">重置</el-button>
                <el-button type="danger" :icon="Delete" :disabled="selectedRows.length === 0" @click="batchRemoveCourses">
                  批量删除
                </el-button>
              </div>
              <el-button class="admin-create-button" type="primary" :icon="Plus" @click="openCreate">新增</el-button>
            </div>
          </div>
        </div>
      </el-form>

      <div class="admin-table-wrap">
        <el-table
          v-loading="loading"
          :data="courses"
          border
          stripe
          class="admin-table"
          @selection-change="handleSelectionChange"
        >
          <el-table-column v-if="isMobile" label="操作" width="150" align="center">
            <template #default="{ row }">
              <el-button type="primary" link :icon="Edit" @click="openEdit(row)">编辑</el-button>
              <el-button type="danger" link :icon="Delete" @click="removeCourse(row)">删除</el-button>
            </template>
          </el-table-column>
          <el-table-column type="selection" width="54" />
          <el-table-column prop="code" label="课程编码" min-width="130" />
          <el-table-column prop="category" label="课程类型" min-width="130">
            <template #default="{ row }">
              <el-tag v-if="row.category" effect="plain">{{ row.category }}</el-tag>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="课程名称" min-width="260" show-overflow-tooltip />
          <el-table-column label="课程链接" min-width="240" show-overflow-tooltip>
            <template #default="{ row }">
              <el-link v-if="row.url" :href="row.url" target="_blank" type="primary">{{ row.url }}</el-link>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="price" label="价格" min-width="100" align="right" />
          <el-table-column prop="modify_time" label="更新时间" min-width="180">
            <template #default="{ row }">{{ formatDate(row.modify_time) }}</template>
          </el-table-column>
          <el-table-column v-if="!isMobile" label="操作" width="180" fixed="right" align="center">
            <template #default="{ row }">
              <el-button type="primary" link :icon="Edit" @click="openEdit(row)">编辑</el-button>
              <el-button type="danger" link :icon="Delete" @click="removeCourse(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination-bar">
        <span>共 {{ total }} 条</span>
        <el-pagination
          v-model:current-page="query.page"
          v-model:page-size="query.page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="sizes, prev, pager, next, jumper"
          background
          @size-change="loadCourses"
          @current-change="loadCourses"
        />
      </div>
    </section>

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑课程' : '新增课程'" width="560px" destroy-on-close>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="88px">
        <el-form-item label="课程编码" prop="code">
          <el-input v-model="form.code" maxlength="50" placeholder="例如 AD-01" />
        </el-form-item>
        <el-form-item label="课程名称" prop="name">
          <el-input v-model="form.name" maxlength="255" placeholder="请输入课程名称" />
        </el-form-item>
        <el-form-item label="课程类型" prop="category">
          <el-input v-model="form.category" maxlength="255" placeholder="例如 Android / Java / 资料" />
        </el-form-item>
        <el-form-item label="课程链接" prop="url">
          <el-input v-model="form.url" maxlength="255" placeholder="https://..." />
        </el-form-item>
        <el-form-item label="课程价格" prop="price">
          <el-input-number v-model="form.price" :min="0" :precision="0" controls-position="right" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="submitCourse">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElButton } from 'element-plus/es/components/button/index.mjs'
import { ElDialog } from 'element-plus/es/components/dialog/index.mjs'
import { ElForm, ElFormItem } from 'element-plus/es/components/form/index.mjs'
import { ElInput } from 'element-plus/es/components/input/index.mjs'
import { ElInputNumber } from 'element-plus/es/components/input-number/index.mjs'
import { ElLink } from 'element-plus/es/components/link/index.mjs'
import { ElPagination } from 'element-plus/es/components/pagination/index.mjs'
import { ElOption, ElSelect } from 'element-plus/es/components/select/index.mjs'
import { ElTable, ElTableColumn } from 'element-plus/es/components/table/index.mjs'
import { ElTag } from 'element-plus/es/components/tag/index.mjs'
import { vLoading } from 'element-plus/es/components/loading/index.mjs'
import { ElMessage } from 'element-plus/es/components/message/index.mjs'
import { ElMessageBox } from 'element-plus/es/components/message-box/index.mjs'
import { Delete, Edit, Plus, RefreshRight, Search } from '@element-plus/icons-vue'

import {
  batchDeleteCoursesApi,
  createCourseApi,
  deleteCourseApi,
  getCategoriesApi,
  getCoursesApi,
  updateCourseApi,
} from '@/api/courses'
import type { Course, CourseForm, CourseQuery } from '@/types/course'

const loading = ref(false)
const saving = ref(false)
const courses = ref<Course[]>([])
const categories = ref<string[]>([])
const selectedRows = ref<Course[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const editingId = ref<number | null>(null)
const formRef = ref<FormInstance>()
const isMobile = ref(false)
let mediaQuery: MediaQueryList | null = null
let syncMobile: (() => void) | null = null

const query = reactive<CourseQuery>({
  code: '',
  name: '',
  category: '',
  price_min: null,
  price_max: null,
  page: 1,
  page_size: 10,
})

const form = reactive<CourseForm>({
  code: '',
  name: '',
  category: '',
  url: '',
  price: 0,
})

const rules: FormRules = {
  code: [{ required: true, message: '请输入课程编码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入课程价格', trigger: 'change' }],
}

async function loadCourses() {
  loading.value = true
  try {
    const { data } = await getCoursesApi(query)
    courses.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

async function loadCategories() {
  const { data } = await getCategoriesApi()
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
  loadCourses()
}

function handleSelectionChange(rows: Course[]) {
  selectedRows.value = rows
}

function resetForm() {
  editingId.value = null
  form.code = ''
  form.name = ''
  form.category = ''
  form.url = ''
  form.price = 0
}

function openCreate() {
  resetForm()
  dialogVisible.value = true
}

function openEdit(row: Course) {
  editingId.value = row.id
  form.code = row.code
  form.name = row.name
  form.category = row.category || ''
  form.url = row.url || ''
  form.price = row.price
  dialogVisible.value = true
}

async function submitCourse() {
  await formRef.value?.validate()
  saving.value = true
  try {
    if (editingId.value) {
      await updateCourseApi(editingId.value, form)
      ElMessage.success('课程已更新')
    } else {
      await createCourseApi(form)
      ElMessage.success('课程已新增')
    }
    dialogVisible.value = false
    await Promise.all([loadCourses(), loadCategories()])
  } finally {
    saving.value = false
  }
}

async function removeCourse(row: Course) {
  await ElMessageBox.confirm(`确认删除课程「${row.name}」吗？`, '删除确认', {
    type: 'warning',
    confirmButtonText: '删除',
    cancelButtonText: '取消',
  })
  await deleteCourseApi(row.id)
  ElMessage.success('课程已删除')
  await Promise.all([loadCourses(), loadCategories()])
}

async function batchRemoveCourses() {
  const ids = selectedRows.value.map((item) => item.id)
  if (ids.length === 0) {
    ElMessage.warning('请先选择要删除的课程')
    return
  }
  await ElMessageBox.confirm(`确认删除选中的 ${ids.length} 门课程吗？`, '批量删除确认', {
    type: 'warning',
    confirmButtonText: '批量删除',
    cancelButtonText: '取消',
  })
  const { data } = await batchDeleteCoursesApi(ids)
  ElMessage.success(`已删除 ${data.deleted} 门课程`)
  selectedRows.value = []
  await Promise.all([loadCourses(), loadCategories()])
}

function formatDate(value: string | null) {
  if (!value) return '-'
  return value.replace('T', ' ').slice(0, 19)
}

onMounted(() => {
  mediaQuery = window.matchMedia('(max-width: 720px)')
  syncMobile = () => {
    isMobile.value = Boolean(mediaQuery?.matches)
  }
  syncMobile()
  mediaQuery.addEventListener('change', syncMobile)
  loadCategories()
  loadCourses()
})

onBeforeUnmount(() => {
  if (mediaQuery && syncMobile) {
    mediaQuery.removeEventListener('change', syncMobile)
  }
})
</script>
