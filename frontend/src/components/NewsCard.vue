<template>
  <article class="news-card" @click="$router.push(`/news/${news.id}`)">
    <div class="card-body" :class="{ 'has-image': news.image }">
      <div class="card-text">
        <h3 class="card-title">{{ news.title }}</h3>
        <p class="card-desc" v-if="news.description">{{ news.description }}</p>
        <div class="card-meta">
          <span class="meta-item" v-if="news.author">{{ news.author }}</span>
          <span class="meta-item">{{ formattedTime }}</span>
          <span class="meta-item">{{ news.views }} 阅读</span>
        </div>
      </div>
      <div class="card-image" v-if="news.image">
        <img :src="news.image" :alt="news.title" loading="lazy" />
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  news: { type: Object, required: true }
})

const formattedTime = computed(() => {
  if (!props.news.publishTime && !props.news.publish_time) return ''
  const date = new Date(props.news.publishTime || props.news.publish_time)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}小时前`
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN')
})
</script>

<style scoped>
.news-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: 16px;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
  border-bottom: 1px solid var(--color-border);
}
.news-card:hover {
  box-shadow: var(--shadow-md);
}
.news-card:last-child {
  border-bottom: none;
}

.card-body {
  display: flex;
  gap: 14px;
}

.card-text {
  flex: 1;
  min-width: 0;
}

.card-title {
  font-size: 17px;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-desc {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: var(--color-text-muted);
}

.card-image {
  width: 120px;
  height: 80px;
  flex-shrink: 0;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--color-bg);
}
.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (max-width: 480px) {
  .card-image {
    width: 100px;
    height: 70px;
  }
  .card-title {
    font-size: 15px;
  }
}
</style>
