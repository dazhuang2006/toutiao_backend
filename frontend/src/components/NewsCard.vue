<template>
  <router-link :to="'/news/' + news.id" class="news-card">
    <div v-if="news.image" class="card-image">
      <img :src="news.image" :alt="news.title" loading="lazy" />
    </div>
    <div class="card-body" :class="{ 'no-image': !news.image }">
      <h3 class="card-title">{{ news.title }}</h3>
      <p v-if="news.description" class="card-desc">{{ news.description }}</p>
      <div class="card-meta">
        <span v-if="news.author" class="meta-author">{{ news.author }}</span>
        <span class="meta-views">{{ news.views }} 阅读</span>
        <span v-if="news.publishTime" class="meta-time">{{ formatTime(news.publishTime) }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({ news: { type: Object, required: true } })
function formatTime(dateStr) {
  if (!dateStr) return ""
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  if (diff < 3600000) return Math.floor(diff / 60000) + "分钟前"
  if (diff < 86400000) return Math.floor(diff / 3600000) + "小时前"
  if (diff < 604800000) return Math.floor(diff / 86400000) + "天前"
  return date.toLocaleDateString("zh-CN", { month: "short", day: "numeric" })
}
</script>

<style scoped>
.news-card {
  display: block; background: var(--surface);
  border-radius: var(--radius-md); overflow: hidden; margin-bottom: 12px;
  box-shadow: var(--shadow-sm); transition: box-shadow 0.15s, transform 0.15s;
}
.news-card:hover { box-shadow: var(--shadow-md); }
.news-card:active { transform: scale(0.985); }
.card-image { width: 100%; aspect-ratio: 16 / 9; overflow: hidden; background: var(--canvas); }
.card-image img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease; }
.news-card:hover .card-image img { transform: scale(1.03); }
.card-body { padding: 14px 16px 16px; }
.card-body.no-image { padding-top: 16px; }
.card-title {
  font-size: 16px; font-weight: 600; line-height: 1.45; color: var(--text);
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.card-desc {
  font-size: 14px; color: var(--text-secondary); line-height: 1.5; margin-top: 6px;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.card-meta {
  display: flex; align-items: center; gap: 12px; margin-top: 10px;
  font-size: 12px; color: var(--text-muted);
}
.meta-author { color: var(--accent); font-weight: 500; }
</style>
