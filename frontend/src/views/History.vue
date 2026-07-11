<template>
  <div class="page history-page">
    <div class="page-header">
      <h1 class="page-title">浏览历史</h1>
      <button v-if="list.length > 0" class="btn btn-sm btn-outline" @click="handleClear">清空</button>
    </div>

    <div v-if="loading" class="loading">加载中</div>
    <div v-else-if="list.length === 0" class="empty">还没有浏览历史</div>

    <template v-else>
      <div v-for="item in list" :key="item.historyId" class="history-item">
        <router-link :to="'/news/' + item.id" class="history-link">
          <div class="history-info">
            <h3 class="history-title">{{ item.title }}</h3>
            <div class="history-meta">
              <span>{{ item.views }} 阅读</span>
              <span>{{ formatTime(item.viewTime) }}</span>
            </div>
          </div>
          <img v-if="item.image" :src="item.image" class="history-thumb" loading="lazy" />
        </router-link>
        <button class="history-del" @click="handleDelete(item.historyId)" title="删除">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
        </button>
      </div>

      <div class="load-more" v-if="hasMore">
        <button class="btn btn-outline" @click="loadMore" :disabled="loadingMore">
          {{ loadingMore ? "加载中..." : "加载更多" }}
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { getHistoryList, deleteHistory, clearHistory } from "@/api/history"

const list = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const page = ref(1)
const hasMore = ref(false)

function formatTime(dateStr) {
  if (!dateStr) return ""
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  if (diff < 3600000) return Math.floor(diff / 60000) + "分钟前"
  if (diff < 86400000) return Math.floor(diff / 3600000) + "小时前"
  return date.toLocaleDateString("zh-CN", { month: "short", day: "numeric" })
}

async function loadHistory() {
  loading.value = true
  page.value = 1
  try {
    const res = await getHistoryList(1)
    list.value = res.data.list
    hasMore.value = res.data.hasMore
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

async function loadMore() {
  loadingMore.value = true
  page.value++
  try {
    const res = await getHistoryList(page.value)
    list.value.push(...res.data.list)
    hasMore.value = res.data.hasMore
  } catch (e) { page.value-- }
  finally { loadingMore.value = false }
}

async function handleDelete(historyId) {
  try {
    await deleteHistory(historyId)
    list.value = list.value.filter(i => i.historyId !== historyId)
  } catch (e) { console.error(e) }
}

async function handleClear() {
  if (!confirm("确定清空所有浏览历史？")) return
  try {
    await clearHistory()
    list.value = []
    hasMore.value = false
  } catch (e) { console.error(e) }
}

onMounted(loadHistory)
</script>

<style scoped>
.history-page { padding-top: calc(var(--header-height) + 8px); }
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.page-title { font-size: 18px; font-weight: 700; color: var(--text); }
.history-item { display: flex; align-items: center; gap: 12px; background: var(--surface); border-radius: var(--radius-sm); padding: 12px 14px; margin-bottom: 8px; box-shadow: var(--shadow-sm); }
.history-link { display: flex; align-items: center; gap: 12px; flex: 1; min-width: 0; }
.history-info { flex: 1; min-width: 0; }
.history-title { font-size: 14px; font-weight: 600; color: var(--text); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }
.history-meta { display: flex; gap: 12px; font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.history-thumb { width: 64px; height: 48px; object-fit: cover; border-radius: 4px; flex-shrink: 0; }
.history-del { flex-shrink: 0; padding: 6px; color: var(--text-muted); border-radius: 50%; transition: color 0.15s; }
.history-del:hover { color: var(--primary); }
.load-more { text-align: center; padding: 16px 0; }
</style>
