<template>
  <div class="page detail-page">
    <div v-if="loading" class="loading">加载中</div>
    <div v-else-if="error" class="empty">{{ error }}</div>

    <template v-else-if="news">
      <article class="detail-card">
        <h1 class="detail-title">{{ news.title }}</h1>

        <div class="detail-meta">
          <span v-if="news.author" class="meta-item author">{{ news.author }}</span>
          <span class="meta-item">{{ formatDate(news.publishTime) }}</span>
          <span class="meta-item">{{ news.views }} 阅读</span>
        </div>

        <img v-if="news.image" :src="news.image" :alt="news.title" class="detail-image" />

        <div v-if="news.summary" class="summary-box">
          <span class="summary-badge">AI 摘要</span>
          <p class="summary-text">{{ news.summary }}</p>
        </div>

        <div class="detail-content" v-html="news.content"></div>

        <div class="detail-actions">
          <button
            :class="['btn', isFavorited ? 'btn-danger' : 'btn-outline']"
            @click="toggleFavorite"
            :disabled="favSubmitting"
          >
            <svg v-if="isFavorited" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
            {{ isFavorited ? "已收藏" : "收藏" }}
          </button>
        </div>
      </article>

      <section class="related-section" v-if="news.relatedNews && news.relatedNews.length > 0">
        <h3 class="section-title">相关推荐</h3>
        <div v-for="item in news.relatedNews" :key="item.id" class="related-item">
          <router-link :to="'/news/' + item.id" class="related-link">
            <span class="related-title">{{ item.title }}</span>
            <span class="related-views">{{ item.views }} 阅读</span>
          </router-link>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import { getNewsDetail } from "@/api/news"
import { checkFavorite, addFavorite, removeFavorite } from "@/api/favorite"
import { addHistory } from "@/api/history"
import { useUserStore } from "@/stores/user"

const route = useRoute()
const { isLoggedIn } = useUserStore()

const news = ref(null)
const loading = ref(true)
const error = ref("")
const isFavorited = ref(false)
const favSubmitting = ref(false)

function formatDate(dateStr) {
  if (!dateStr) return ""
  return new Date(dateStr).toLocaleString("zh-CN", { year: "numeric", month: "long", day: "numeric", hour: "2-digit", minute: "2-digit" })
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
  } catch (e) { console.error(e) }
  finally { favSubmitting.value = false }
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
    error.value = "新闻不存在或加载失败"
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.detail-page { padding-top: calc(var(--header-height) + 8px); }
.detail-card { background: var(--surface); border-radius: var(--radius-md); padding: 24px 20px; box-shadow: var(--shadow-sm); }
.detail-title { font-size: 22px; font-weight: 700; line-height: 1.4; margin-bottom: 12px; color: var(--text); }
.detail-meta { display: flex; gap: 16px; font-size: 13px; color: var(--text-muted); margin-bottom: 20px; flex-wrap: wrap; }
.meta-item.author { color: var(--accent); font-weight: 500; }
.detail-image { width: 100%; max-height: 400px; object-fit: cover; border-radius: var(--radius-sm); margin-bottom: 20px; }
.summary-box { background: var(--accent-soft); border-radius: var(--radius-sm); padding: 16px; margin-bottom: 20px; border-left: 3px solid var(--accent); }
.summary-badge { display: inline-block; font-size: 11px; font-weight: 600; color: var(--accent); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.summary-text { font-size: 15px; line-height: 1.7; color: var(--text-secondary); }
.detail-content { font-size: 16px; line-height: 1.8; color: var(--text); margin-bottom: 20px; }
.detail-content :deep(p) { margin-bottom: 16px; }
.detail-content :deep(img) { border-radius: var(--radius-xs); margin: 16px 0; }
.detail-actions { display: flex; gap: 12px; padding-top: 16px; border-top: 1px solid var(--border); }
.related-section { margin-top: 28px; }
.section-title { font-size: 17px; font-weight: 600; margin-bottom: 12px; padding-left: 12px; border-left: 3px solid var(--primary); color: var(--text); }
.related-item { padding: 12px 0; border-bottom: 1px solid var(--border); }
.related-link { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.related-title { font-size: 14px; font-weight: 500; color: var(--text); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.related-views { font-size: 12px; color: var(--text-muted); flex-shrink: 0; }
@media (max-width: 480px) { .detail-card { padding: 20px 16px; } .detail-title { font-size: 20px; } }
</style>
