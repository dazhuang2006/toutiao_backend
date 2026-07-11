<template>
  <header class="app-header">
    <div class="header-inner">
      <router-link to="/" class="logo">
        <span class="logo-icon">&#9670;</span>
        <span class="logo-text">AI 头条</span>
      </router-link>
      <div class="header-right">
        <router-link v-if="!isLoggedIn" to="/login" class="login-btn">登录</router-link>
        <router-link v-else to="/profile" class="avatar-link">
          <img v-if="userInfo?.avatar" :src="userInfo.avatar" class="avatar" />
          <span v-else class="avatar-placeholder">{{ userInfo?.username?.[0] || "U" }}</span>
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useUserStore } from "@/stores/user"
const { isLoggedIn, userInfo } = useUserStore()
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: var(--header-height);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  z-index: 100;
}
.header-inner {
  max-width: var(--max-width);
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}
.logo { display: flex; align-items: center; gap: 8px; }
.logo-icon { font-size: 22px; color: var(--primary); line-height: 1; }
.logo-text { font-size: 18px; font-weight: 700; color: var(--text); letter-spacing: -0.3px; }
.login-btn {
  font-size: 14px; font-weight: 500; color: var(--accent);
  padding: 6px 14px; border: 1px solid var(--accent); border-radius: var(--radius-pill);
  transition: all 0.15s;
}
.login-btn:hover { background: var(--accent); color: #fff; }
.avatar-link { display: flex; align-items: center; }
.avatar { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; }
.avatar-placeholder {
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--primary); color: #fff; display: flex;
  align-items: center; justify-content: center;
  font-size: 14px; font-weight: 600;
}
</style>
