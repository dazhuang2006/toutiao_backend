<template>
  <div class="page fav-page">
    <div class="page-header">
      <h1 class="page-title">我的收藏</h1>
      <button v-if="list.length > 0" class="btn btn-sm btn-outline" @click="handleClear">清空</button>
    </div>

    <div v-if="loading" class="loading">加载中</div>
    <div v-else-if="list.length === 0" class="empty">还没有收藏任何新闻</div>

    <template v-else>
      <NewsCard v-for="item in list" :key="item.id" :news="item" />

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
import { getFavoriteList, clearFavorites } from "@/api/favorite"
import NewsCard from "@/components/NewsCard.vue"

const list = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const page = ref(1)
const hasMore = ref(false)

async function loadFavs() {
  loading.value = true
  page.value = 1
  try {
    const res = await getFavoriteList(1)
    list.value = res.data.list
    hasMore.value = res.data.hasMore
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

async function loadMore() {
  loadingMore.value = true
  page.value++
  try {
    const res = await getFavoriteList(page.value)
    list.value.push(...res.data.list)
    hasMore.value = res.data.hasMore
  } catch (e) { page.value-- }
  finally { loadingMore.value = false }
}

async function handleClear() {
  if (!confirm("确定清空所有收藏？")) return
  try {
    await clearFavorites()
    list.value = []
    hasMore.value = false
  } catch (e) { console.error(e) }
}

onMounted(loadFavs)
</script>

<style scoped>
.fav-page { padding-top: calc(var(--header-height) + 8px); }
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.page-title { font-size: 18px; font-weight: 700; color: var(--text); }
.load-more { text-align: center; padding: 16px 0; }
</style>
