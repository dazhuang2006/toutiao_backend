<template>
  <div class="page detail-page">
    <div v-if="loading" class="loading">加载中</div>
    <div v-else-if="error" class="empty">{{ error }}</div>
    <template v-else-if="news">
      <article class="detail-card">
        <h1 class="detail-title">{{ news.title }}</h1>
        <div class="detail-meta">
          <span v-if="news.author" class="meta-item">{{ news.author }}</span>
          <span class="meta-item">{{ formatDate(news.publishTime) }}</span>
          <span class="meta-item">{{ news.views }} 阅读</span>
        </div>
        <img v-if="news.image" :src="news.image" :alt="news.title" class="detail-image" />
        <div class="detail-content" v-html="news.content"></div>
        <div class="detail-actions">
          <button
            :class="['btn', isFavorited ? 'btn-danger' : 'btn-outline']"
            @click="toggleFavorite"
            :disabled="favSubmitting"
          >
            {{ isFavorited ? '取消收藏' : '收藏' }}
          </button>
        </div>
      </article>

      <section class="related-section" v-if="news.relatedNews && news.relatedNews.length > 0">
        <h3 class="section-title">相关推荐</h3>
        <NewsCard v-for="item in news.relatedNews" :key="item.id" :news="item" />
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getNewsDetail } from '@/api/news'
import { checkFavorite, addFavorite, removeFavorite } from '@/api/favorite'
import { addHistory } from '@/api/history'
import { useUserStore } from '@/stores/user'
import NewsCard from '@/components/NewsCard.vue'

const route = useRoute()
const { isLoggedIn } = useUserStore()

const news = ref(null)
const loading = ref(true)
const error = ref('')
const isFavorited = ref(false)
const favSubmitting = ref(false)

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

async function toggleFavorite() {
  if (!isLoggedIn.value) return
  favSubmitting.value = true
  try {
    if (isFavorited.value) {
      await removeFavorite(news.value.id)
      isFavorited.value = false
    } else {
      await addFavorite(news.value.id)
      isFavorited.value = true
    }
  } catch (e) {
    console.error(e)
  } finally {
    favSubmitting.value = false
  }
}

onMounted(async () => {
  try {
    const res = await getNewsDetail(route.params.id)
    news.value = res.data
    if (isLoggedIn.value) {
      try {
        const favRes = await checkFavorite(news.value.id)
        isFavorited.value = favRes.data.isFavorite
      } catch (e) { /* ignore */ }
      try {
        await addHistory(news.value.id)
      } catch (e) { /* ignore */ }
    }
  } catch (e) {
    error.value = '新闻不存在或加载失败'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.detail-page {
  padding-top: calc(var(--header-height) + 16px);
}

.detail-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 28px 24px;
}

.detail-title {
  font-size: 24px;
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: 14px;
}

.detail-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.detail-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  border-radius: var(--radius-md);
  margin-bottom: 24px;
}

.detail-content {
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-text);
  margin-bottom: 24px;
}

.detail-actions {
  display: flex;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.related-section {
  margin-top: 28px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 14px;
  padding-left: 12px;
  border-left: 3px solid var(--color-primary);
}

@media (max-width: 480px) {
  .detail-card {
    padding: 20px 16px;
  }
  .detail-title {
    font-size: 20px;
  }
}
</style>
