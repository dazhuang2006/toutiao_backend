<template>
  <div class="page detail-page">
    <div v-if="loading" class="loading">加载中</div>
    <div v-else-if="error" class="empty">{{ error }}</div>

    <template v-else-if="news">
      <article class="article">
        <header class="article-header">
          <div class="article-kicker mono">Latest / 新闻详情</div>
          <h1 class="article-title">{{ news.title }}</h1>
          <div class="article-meta mono">
            <span v-if="news.author">{{ news.author }}</span>
            <span>{{ formatDate(news.publishTime) }}</span>
            <span>{{ news.views }} 阅读</span>
          </div>
        </header>

        <img v-if="news.image" :src="news.image" :alt="news.title" class="article-image" />

        <div v-if="news.summary" class="ai-panel">
          <div class="ai-badge mono">AI 摘要 // Generated</div>
          <p class="ai-text">{{ news.summary }}</p>
        </div>

        <div class="article-content" v-html="news.content"></div>

        <div class="article-actions">
          <button
            :class="['btn', isFavorited ? 'btn-primary' : 'btn-outline']"
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
        <h2 class="related-title mono">Related / 相关推荐</h2>
        <router-link v-for="(item, i) in news.relatedNews" :key="item.id" :to="'/news/' + item.id" class="related-row">
          <span class="related-index mono">{{ String(i + 1).padStart(2, "0") }}</span>
          <span class="related-headline">{{ item.title }}</span>
          <span class="related-views mono">{{ item.views }} 阅读</span>
        </router-link>
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
.detail-page { padding-top: calc(var(--header-height) + 20px); max-width: 960px; }
.article { border: 1px solid var(--hairline); background: var(--canvas-soft); }
.article-header { padding: 36px 36px 0; }
.article-kicker { font-size: 11px; color: var(--mint); margin-bottom: 14px; }
.article-title { font-size: 40px; font-weight: 800; line-height: 1.18; color: var(--text); }
.article-meta { display: flex; gap: 18px; font-size: 11px; color: var(--text-muted); margin-top: 18px; padding-bottom: 24px; border-bottom: 1px solid var(--hairline); flex-wrap: wrap; }
.article-image { width: 100%; max-height: 460px; object-fit: cover; border-bottom: 1px solid var(--hairline); margin-top: 24px; }
.ai-panel { margin: 28px 36px 0; background: var(--black); border: 1px solid var(--mint); border-left: 4px solid var(--mint); padding: 18px 20px; }
.ai-badge { font-size: 10px; color: var(--mint); margin-bottom: 10px; }
.ai-text { font-size: 16px; line-height: 1.8; color: var(--text-secondary); }
.article-content { padding: 28px 36px 36px; font-size: 17px; line-height: 1.95; color: var(--text); }
.article-content :deep(p) { margin-bottom: 18px; }
.article-content :deep(img) { margin: 20px 0; border: 1px solid var(--hairline); }
.article-actions { padding: 0 36px 36px; display: flex; gap: 12px; }
.related-section { margin-top: 36px; }
.related-title { font-size: 12px; color: var(--text-muted); margin-bottom: 12px; }
.related-row { display: flex; align-items: center; gap: 16px; padding: 16px 4px; border-bottom: 1px solid var(--hairline); }
.related-row:hover .related-headline { color: var(--mint); }
.related-index { font-size: 11px; color: var(--mint); }
.related-headline { font-size: 16px; font-weight: 700; flex: 1; }
.related-views { font-size: 10px; color: var(--text-muted); }
@media (max-width: 768px) {
  .article-header { padding: 24px 20px 0; }
  .article-title { font-size: 28px; }
  .ai-panel { margin: 20px 20px 0; }
  .article-content { padding: 20px; font-size: 16px; }
  .article-actions { padding: 0 20px 24px; }
}
</style>
