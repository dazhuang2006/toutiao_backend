<template>
  <div class="page auth-page">
    <div class="auth-card">
      <h2 class="auth-title">登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <input v-model="username" class="input" placeholder="用户名" required />
        </div>
        <div class="form-group">
          <input v-model="password" class="input" type="password" placeholder="密码" required />
        </div>
        <p class="error-text" v-if="error">{{ error }}</p>
        <button type="submit" class="btn btn-primary btn-block" :disabled="submitting">
          {{ submitting ? '登录中...' : '登录' }}
        </button>
      </form>
      <p class="auth-footer">
        还没有账号？<router-link to="/register" class="link">立即注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { login } from '@/api/user'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const { setLogin } = useUserStore()

const username = ref('')
const password = ref('')
const error = ref('')
const submitting = ref(false)

async function handleLogin() {
  error.value = ''
  submitting.value = true
  try {
    const res = await login(username.value, password.value)
    setLogin(res.data.token, res.data.userInfo)
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (e) {
    error.value = e.response?.data?.detail || '登录失败，请检查用户名和密码'
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
