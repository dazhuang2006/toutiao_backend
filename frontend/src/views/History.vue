<template>
  <div class="page history-page">
    <div class="page-header">
      <h2>浏览历史</h2>
      <button class="btn btn-danger btn-sm" v-if="list.length > 0" @click="handleClear">清空历史</button>
    </div>

    <div v-if="loading" class="loading">加载中</div>
    <div v-else-if="list.length === 0" class="empty">暂无浏览记录</div>
    <template v-else>
      <div v-for="item in list" :key="item.historyId || item.id" class="history-item">
        <NewsCard :news="item" />
        <button class="delete-btn" @click.stop="handleDelete(item.historyId)">删除</button>
      </div>
      <div class="load-more" v-if="hasMore">
        <button class="btn btn-outline" @click="loadMore" :disabled="loadingMore">
          {{ loadingMore ? '加载中...' : '加载更多' }}
        </button>
      </div>
      <div v-else-if="list.length > 0" class="no-more">— 没有更多了 —</div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getHistoryList, deleteHistory, clearHistory } from '@/api/history'
import NewsCard from '@/components/NewsCard.vue'

const list = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const page = ref(1)
const hasMore = ref(false)

async function loadData() {
  loading.value = true
  page.value = 1
  try {
    const res = await getHistoryList(1)
    list.value = res.data.list
    hasMore.value = res.data.hasMore
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function loadMore() {
  loadingMore.value = true
  page.value++
  try {
    const res = await getHistoryList(page.value)
    list.value.push(...res.data.list)
    hasMore.value = res.data.hasMore
  } catch (e) {
    page.value--
  } finally {
    loadingMore.value = false
  }
}

async function handleDelete(historyId) {
  await deleteHistory(historyId)
  list.value = list.value.filter(item => (item.historyId || item.history_id) !== historyId)
}

async function handleClear() {
  await clearHistory()
  list.value = []
  hasMore.value = false
}

onMounted(loadData)
</script>

<style scoped>
.history-page {
  padding-top: calc(var(--header-height) + 16px);
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.page-header h2 {
  font-size: 20px;
  font-weight: 600;
}

.history-item {
  position: relative;
}

.delete-btn {
  position: absolute;
  right: 12px;
  bottom: 12px;
  font-size: 12px;
  color: var(--color-text-muted);
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
}
.delete-btn:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.load-more {
  text-align: center;
  padding: 20px 0;
}

.no-more {
  text-align: center;
  padding: 24px 0;
  color: var(--color-text-muted);
  font-size: 13px;
}
</style>
