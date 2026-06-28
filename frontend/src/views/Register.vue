<template>
  <div class="page auth-page">
    <div class="auth-card">
      <h2 class="auth-title">注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <input v-model="username" class="input" placeholder="用户名" required />
        </div>
        <div class="form-group">
          <input v-model="password" class="input" type="password" placeholder="密码" required minlength="6" />
        </div>
        <div class="form-group">
          <input v-model="confirmPassword" class="input" type="password" placeholder="确认密码" required />
        </div>
        <p class="error-text" v-if="error">{{ error }}</p>
        <button type="submit" class="btn btn-primary btn-block" :disabled="submitting">
          {{ submitting ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="auth-footer">
        已有账号？<router-link to="/login" class="link">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/user'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const { setLogin } = useUserStore()

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const submitting = ref(false)

async function handleRegister() {
  error.value = ''
  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  if (password.value.length < 6) {
    error.value = '密码长度至少6位'
    return
  }
  submitting.value = true
  try {
    const res = await register(username.value, password.value)
    setLogin(res.data.token, res.data.userInfo)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || '注册失败'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: calc(var(--header-height) + 60px);
}

.auth-card {
  width: 100%;
  max-width: 380px;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 36px 28px;
  box-shadow: var(--shadow-sm);
}

.auth-title {
  font-size: 22px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 28px;
}

.form-group {
  margin-bottom: 16px;
}

.btn-block {
  width: 100%;
  margin-top: 8px;
}

.auth-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.link {
  color: var(--color-primary);
  font-weight: 500;
}
.link:hover {
  text-decoration: underline;
}
</style>
