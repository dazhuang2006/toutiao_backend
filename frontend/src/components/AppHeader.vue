<template>
  <header class="app-header">
    <div class="header-inner">
      <router-link to="/" class="brand">
        <span class="brand-mark">◆</span>
        <span class="brand-name">AI 头条</span>
        <span class="brand-tag mono">News Desk</span>
      </router-link>

      <nav class="header-nav">
        <router-link to="/" class="nav-link">首页</router-link>
        <router-link to="/ask" class="nav-link">AI 问</router-link>
        <router-link v-if="isLoggedIn" to="/favorites" class="nav-link">收藏</router-link>
        <router-link v-if="isLoggedIn" to="/history" class="nav-link">历史</router-link>
      </nav>

      <div class="header-right">
        <router-link v-if="!isLoggedIn" to="/login" class="btn btn-primary btn-sm">登录</router-link>
        <router-link v-else to="/profile" class="avatar-link">
          <img v-if="userInfo?.avatar" :src="userInfo.avatar" class="avatar" alt="avatar" />
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
  background: var(--canvas);
  border-bottom: 1px solid var(--hairline);
  z-index: 100;
}
.header-inner {
  max-width: var(--max-width);
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 0 24px;
}
.brand { display: flex; align-items: center; gap: 10px; }
.brand-mark { color: var(--mint); font-size: 18px; line-height: 1; }
.brand-name { font-size: 22px; font-weight: 800; color: var(--text); }
.brand-tag { font-size: 10px; color: var(--mint); border: 1px solid var(--mint); padding: 2px 6px; }
.header-nav { display: flex; align-items: center; gap: 4px; }
.nav-link {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: 8px 12px;
  border-bottom: 2px solid transparent;
  transition: color 0.12s, border-color 0.12s;
}
.nav-link:hover { color: var(--mint); }
.nav-link.router-link-active { color: var(--text); border-bottom-color: var(--mint); }
.header-right { display: flex; align-items: center; }
.avatar-link { display: flex; align-items: center; }
.avatar { width: 34px; height: 34px; object-fit: cover; border: 1px solid var(--mint); }
.avatar-placeholder {
  width: 34px; height: 34px;
  background: var(--uv-soft); color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700;
  border: 1px solid var(--mint);
}
@media (max-width: 768px) {
  .header-nav, .brand-tag { display: none; }
  .header-inner { padding: 0 16px; }
}
</style>
