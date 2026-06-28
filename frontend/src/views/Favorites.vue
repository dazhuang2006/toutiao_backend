<template>
  <div class="page fav-page">
    <div class="page-header">
      <h2>我的收藏</h2>
      <button class="btn btn-danger btn-sm" v-if="list.length > 0" @click="handleClear">清空收藏</button>
    </div>

    <div v-if="loading" class="loading">加载中</div>
    <div v-else-if="list.length === 0" class="empty">暂无收藏</div>
    <template v-else>
      <NewsCard v-for="item in list" :key="item.favoriteId || item.id" :news="item" />
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
import { getFavoriteList, clearFavorites } from '@/api/favorite'
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
    const res = await getFavoriteList(1)
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
    const res = await getFavoriteList(page.value)
    list.value.push(...res.data.list)
    hasMore.value = res.data.hasMore
  } catch (e) {
    page.value--
  } finally {
    loadingMore.value = false
  }
}

async function handleClear() {
  await clearFavorites()
  list.value = []
  hasMore.value = false
}

onMounted(loadData)
</script>

<style scoped>
.fav-page {
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
