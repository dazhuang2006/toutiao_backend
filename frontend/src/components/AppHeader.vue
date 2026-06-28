<template>
  <header class="header">
    <div class="header-inner">
      <router-link to="/" class="logo">今日头条</router-link>
      <nav class="nav">
        <template v-if="isLoggedIn">
          <router-link to="/favorites" class="nav-link">收藏</router-link>
          <router-link to="/history" class="nav-link">历史</router-link>
          <router-link to="/profile" class="nav-link user-link">
            <span class="avatar-mini">{{ userInfo.username.charAt(0).toUpperCase() }}</span>
            <span>{{ userInfo.username }}</span>
          </router-link>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link">登录</router-link>
          <router-link to="/register" class="btn btn-primary btn-sm">注册</router-link>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
const { isLoggedIn, userInfo } = useUserStore()
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--header-height);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
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

.logo {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-primary);
  letter-spacing: 1px;
}

.nav {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-link {
  font-size: 14px;
  color: var(--color-text-secondary);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  transition: color 0.2s;
}
.nav-link:hover {
  color: var(--color-primary);
}

.user-link {
  display: flex;
  align-items: center;
  gap: 6px;
}

.avatar-mini {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
}
</style>
