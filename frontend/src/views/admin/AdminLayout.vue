<template>
  <el-config-provider :locale="zhCn">
    <el-container class="admin-shell">
      <div class="admin-board">
        <el-header class="admin-header">
          <h1>课程管理系统后台</h1>
          <div class="header-actions">
            <el-button :icon="House" @click="$router.push('/')">前台首页</el-button>
            <el-dropdown @command="handleCommand">
              <button class="user-button">
                <el-icon><UserFilled /></el-icon>
                <span>{{ auth.username || '管理员' }}</span>
              </button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="password">修改密码</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main class="admin-main">
          <RouterView />
        </el-main>
      </div>

      <el-dialog v-model="passwordDialogVisible" title="修改密码" width="440px" destroy-on-close>
        <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="96px">
          <el-form-item label="原密码" prop="oldPassword">
            <el-input v-model="passwordForm.oldPassword" type="password" show-password placeholder="请输入原密码" />
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="至少 6 位" />
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="passwordDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="passwordSaving" @click="submitPassword">保存</el-button>
        </template>
      </el-dialog>
    </el-container>
  </el-config-provider>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElButton } from 'element-plus/es/components/button/index.mjs'
import { ElConfigProvider } from 'element-plus/es/components/config-provider/index.mjs'
import { ElContainer, ElHeader, ElMain } from 'element-plus/es/components/container/index.mjs'
import { ElDialog } from 'element-plus/es/components/dialog/index.mjs'
import { ElDropdown, ElDropdownItem, ElDropdownMenu } from 'element-plus/es/components/dropdown/index.mjs'
import { ElForm, ElFormItem } from 'element-plus/es/components/form/index.mjs'
import { ElIcon } from 'element-plus/es/components/icon/index.mjs'
import { ElInput } from 'element-plus/es/components/input/index.mjs'
import { ElMessage } from 'element-plus/es/components/message/index.mjs'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { House, UserFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

import { changePasswordApi } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'
import '@/styles/element-admin.css'

const router = useRouter()
const auth = useAuthStore()
const passwordDialogVisible = ref(false)
const passwordSaving = ref(false)
const passwordFormRef = ref<FormInstance>()

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const validateConfirmPassword = (_rule: unknown, value: string, callback: (error?: Error) => void) => {
  if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入的新密码不一致'))
    return
  }
  callback()
}

const passwordRules: FormRules = {
  oldPassword: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '新密码至少 6 位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' },
  ],
}

function resetPasswordForm() {
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  passwordFormRef.value?.clearValidate()
}

function openPasswordDialog() {
  resetPasswordForm()
  passwordDialogVisible.value = true
}

async function submitPassword() {
  await passwordFormRef.value?.validate()
  passwordSaving.value = true
  try {
    await changePasswordApi(passwordForm.oldPassword, passwordForm.newPassword)
    ElMessage.success('密码已修改，请重新登录')
    passwordDialogVisible.value = false
    auth.logout()
    router.push('/login')
  } finally {
    passwordSaving.value = false
  }
}

function handleCommand(command: string) {
  if (command === 'password') {
    openPasswordDialog()
    return
  }
  if (command === 'logout') {
    auth.logout()
    router.push('/login')
  }
}
</script>
