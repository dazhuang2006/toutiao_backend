<template>
  <div class="page home-page">
    <CategoryTabs :categories="categories" :activeId="activeCategory" @select="switchCategory" />

    <div v-if="loading" class="loading">加载中</div>
    <div v-else-if="newsList.length === 0" class="empty">暂无新闻</div>

    <template v-else>
      <NewsCard v-for="item in newsList" :key="item.id" :news="item" />

      <div class="load-more" v-if="hasMore">
        <button class="btn btn-outline" @click="loadMore" :disabled="loadingMore">
          {{ loadingMore ? "加载中..." : "加载更多" }}
        </button>
      </div>
      <div v-else-if="newsList.length > 0" class="no-more">&mdash; 没有更多了 &mdash;</div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { getCategories, getNewsList } from "@/api/news"
import CategoryTabs from "@/components/CategoryTabs.vue"
import NewsCard from "@/components/NewsCard.vue"

const categories = ref([])
const activeCategory = ref(0)
const newsList = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const page = ref(1)
const hasMore = ref(false)

async function loadCategories() {
  try {
    const res = await getCategories()
    categories.value = res.data
    if (res.data.length > 0) {
      activeCategory.value = res.data[0].id
      await loadNews()
    }
  } catch (e) {
    console.error(e)
    loading.value = false
  }
}

async function loadNews() {
  loading.value = true
  page.value = 1
  try {
    const res = await getNewsList(activeCategory.value, 1)
    newsList.value = res.data.list
    hasMore.value = res.data.hasMore
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

async function switchCategory(id) {
  activeCategory.value = id
  await loadNews()
}

async function loadMore() {
  loadingMore.value = true
  page.value++
  try {
    const res = await getNewsList(activeCategory.value, page.value)
    newsList.value.push(...res.data.list)
    hasMore.value = res.data.hasMore
  } catch (e) { page.value-- }
  finally { loadingMore.value = false }
}

onMounted(loadCategories)
</script>

<style scoped>
.home-page { padding-top: calc(var(--header-height)); padding-bottom: 20px; }
.load-more { text-align: center; padding: 20px 0; }
.no-more { text-align: center; padding: 24px 0; color: var(--text-muted); font-size: 13px; }
</style>
