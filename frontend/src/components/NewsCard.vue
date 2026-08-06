<template>
  <router-link :to="'/news/' + news.id" :class="['news-card', { hero, 'tile-accent': !news.image }]" :data-accent="accent">
    <div v-if="news.image" class="card-image">
      <img :src="news.image" :alt="news.title" loading="lazy" />
    </div>
    <div class="card-body">
      <div class="card-kicker mono">{{ news.author || "News Desk" }}</div>
      <h3 class="card-title">{{ news.title }}</h3>
      <p v-if="news.description" class="card-desc">{{ news.description }}</p>
      <div class="card-meta mono">
        <span>{{ news.views }} 阅读</span>
        <span v-if="news.publishTime">{{ formatTime(news.publishTime) }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  news: { type: Object, required: true },
  hero: { type: Boolean, default: false },
})

const accent = computed(() => Math.abs(props.news.id || 0) % 7)

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
  display: flex; flex-direction: column;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: var(--surface);
  min-height: 100%;
  transition: border-color 0.12s ease;
}
.news-card:hover { border-color: var(--mint); }
.card-image { width: 100%; aspect-ratio: 16 / 9; overflow: hidden; background: var(--black); border-bottom: 1px solid rgba(255, 255, 255, 0.3); }
.card-image img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease; }
.news-card:hover .card-image img { transform: scale(1.03); }
.card-body { display: flex; flex-direction: column; gap: 10px; padding: 18px 20px 20px; flex: 1; }
.card-kicker { font-size: 10px; font-weight: 600; color: var(--mint); }
.card-title {
  font-size: 22px; font-weight: 800; line-height: 1.25; color: var(--text);
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.news-card:hover .card-title { color: var(--mint); }
.card-desc {
  font-size: 14px; color: var(--text-secondary); line-height: 1.55;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.card-meta {
  display: flex; align-items: center; gap: 14px; margin-top: auto;
  font-size: 10px; color: var(--text-muted);
}
.news-card.hero .card-title { font-size: 34px; -webkit-line-clamp: 3; }
.news-card.hero .card-image { aspect-ratio: 21 / 9; }

.news-card.tile-accent { border-color: var(--black); }
.tile-accent[data-accent="0"] { background: var(--mint); }
.tile-accent[data-accent="1"] { background: var(--uv-soft); }
.tile-accent[data-accent="2"] { background: var(--tile-yellow); }
.tile-accent[data-accent="3"] { background: var(--tile-pink); }
.tile-accent[data-accent="4"] { background: var(--tile-orange); }
.tile-accent[data-accent="5"] { background: var(--tile-blue); }
.tile-accent[data-accent="6"] { background: var(--tile-white); }

.tile-accent[data-accent="0"] .card-title,
.tile-accent[data-accent="2"] .card-title,
.tile-accent[data-accent="3"] .card-title,
.tile-accent[data-accent="4"] .card-title,
.tile-accent[data-accent="6"] .card-title { color: var(--black); }
.tile-accent[data-accent="0"] .card-kicker,
.tile-accent[data-accent="2"] .card-kicker,
.tile-accent[data-accent="3"] .card-kicker,
.tile-accent[data-accent="4"] .card-kicker,
.tile-accent[data-accent="6"] .card-kicker { color: var(--black); }
.tile-accent[data-accent="0"] .card-desc,
.tile-accent[data-accent="2"] .card-desc,
.tile-accent[data-accent="3"] .card-desc,
.tile-accent[data-accent="4"] .card-desc,
.tile-accent[data-accent="6"] .card-desc { color: rgba(0, 0, 0, 0.72); }
.tile-accent[data-accent="0"] .card-meta,
.tile-accent[data-accent="2"] .card-meta,
.tile-accent[data-accent="3"] .card-meta,
.tile-accent[data-accent="4"] .card-meta,
.tile-accent[data-accent="6"] .card-meta { color: rgba(0, 0, 0, 0.6); }
.tile-accent[data-accent="0"]:hover .card-title,
.tile-accent[data-accent="2"]:hover .card-title,
.tile-accent[data-accent="3"]:hover .card-title,
.tile-accent[data-accent="4"]:hover .card-title,
.tile-accent[data-accent="6"]:hover .card-title { color: var(--link-hover); }
</style>
