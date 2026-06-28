<template>
  <div class="page home">
    <div class="categories">
      <button
        v-for="cat in categories"
        :key="cat.id"
        :class="['cat-btn', { active: activeCategory === cat.id }]"
        @click="switchCategory(cat.id)"
      >{{ cat.name }}</button>
    </div>

    <div v-if="loading" class="loading">加载中</div>

    <div v-else-if="newsList.length === 0" class="empty">暂无新闻</div>

    <template v-else>
      <NewsCard v-for="item in newsList" :key="item.id" :news="item" />
      <div class="load-more" v-if="hasMore">
        <button class="btn btn-outline" @click="loadMore" :disabled="loadingMore">
          {{ loadingMore ? '加载中...' : '加载更多' }}
        </button>
      </div>
      <div v-else class="no-more">— 没有更多了 —</div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategories, getNewsList } from '@/api/news'
import NewsCard from '@/components/NewsCard.vue'

const categories = ref([])
const activeCategory = ref(0)
const newsList = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const page = ref(1)
const hasMore = ref(false)

async function loadCategories() {
  const res = await getCategories()
  categories.value = res.data
  if (res.data.length > 0) {
    activeCategory.value = res.data[0].id
    await loadNews()
  }
}

async function loadNews() {
  loading.value = true
  page.value = 1
  try {
    const res = await getNewsList(activeCategory.value, 1)
    newsList.value = res.data.list
    hasMore.value = res.data.hasMore
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
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
  } catch (e) {
    page.value--
  } finally {
    loadingMore.value = false
  }
}

onMounted(loadCategories)
</script>

<style scoped>
.home {
  padding-top: calc(var(--header-height) + 8px);
}

.categories {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 12px 0;
  margin-bottom: 8px;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.categories::-webkit-scrollbar {
  display: none;
}

.cat-btn {
  flex-shrink: 0;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  transition: all 0.2s;
}
.cat-btn:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}
.cat-btn.active {
  background: var(--color-primary);
  color: #fff;
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
