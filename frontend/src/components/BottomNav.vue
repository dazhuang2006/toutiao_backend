<template>
  <nav class="bottom-nav">
    <router-link v-for="tab in tabs" :key="tab.path" :to="tab.path"
      class="nav-item" :class="{ active: $route.path === tab.path }">
      <span class="nav-icon" v-html="tab.icon"></span>
      <span class="nav-label">{{ tab.label }}</span>
    </router-link>
  </nav>
</template>

<script setup>
const tabs = [
  { path: "/", label: "首页", icon: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>' },
  { path: "/favorites", label: "收藏", icon: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>' },
  { path: "/history", label: "历史", icon: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>' },
  { path: "/profile", label: "我的", icon: '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>' },
]
</script>

<style scoped>
.bottom-nav {
  position: fixed; bottom: 0; left: 0; right: 0;
  height: var(--bottom-nav-height);
  background: var(--surface); border-top: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-around;
  z-index: 100; padding-bottom: env(safe-area-inset-bottom, 0);
}
.nav-item {
  display: flex; flex-direction: column; align-items: center; gap: 2px;
  padding: 6px 12px; color: var(--text-muted); transition: color 0.15s;
  -webkit-tap-highlight-color: transparent;
}
.nav-item.active { color: var(--primary); }
.nav-icon { display: flex; align-items: center; justify-content: center; height: 24px; }
.nav-label { font-size: 10px; font-weight: 500; }
</style>
