<template>
  <div class="page auth-page">
    <div class="auth-card">
      <div class="auth-kicker mono">Member Access</div>
      <h1 class="auth-title">登录</h1>
      <p class="auth-subtitle">登录你的 AI 头条账号</p>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <input v-model="username" class="input" placeholder="请输入用户名" required />
        </div>
        <div class="form-group">
          <label class="form-label">密码</label>
          <input v-model="password" type="password" class="input" placeholder="请输入密码" required />
        </div>
        <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>
        <button type="submit" class="btn btn-primary auth-btn" :disabled="submitting">
          {{ submitting ? "登录中..." : "登录" }}
        </button>
      </form>
      <p class="auth-footer">
        还没有账号？<router-link to="/register" class="auth-link">立即注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter, useRoute } from "vue-router"
import { login } from "@/api/user"
import { useUserStore } from "@/stores/user"

const router = useRouter()
const route = useRoute()
const { setLogin } = useUserStore()

const username = ref("")
const password = ref("")
const errorMsg = ref("")
const submitting = ref(false)

async function handleLogin() {
  errorMsg.value = ""
  submitting.value = true
  try {
    const res = await login(username.value, password.value)
    setLogin(res.data.token, res.data.userInfo)
    const redirect = route.query.redirect || "/"
    router.push(redirect)
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || "登录失败，请检查用户名和密码"
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.auth-page { display: flex; align-items: flex-start; justify-content: center; padding-top: 60px; }
.auth-card { background: var(--canvas-soft); border: 1px solid var(--hairline-bright); padding: 36px 32px; width: 100%; max-width: 420px; }
.auth-kicker { font-size: 10px; color: var(--mint); margin-bottom: 10px; }
.auth-title { font-size: 32px; font-weight: 800; color: var(--text); margin-bottom: 4px; }
.auth-subtitle { font-size: 14px; color: var(--text-muted); margin-bottom: 24px; }
.form-group { margin-bottom: 16px; }
.form-label { display: block; font-family: var(--font-mono); font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 6px; }
.auth-btn { width: 100%; margin-top: 8px; padding: 10px; font-size: 15px; }
.auth-footer { text-align: center; margin-top: 20px; font-size: 14px; color: var(--text-muted); }
.auth-link { color: var(--mint); font-weight: 600; }
.auth-link:hover { text-decoration: underline; }
</style>
