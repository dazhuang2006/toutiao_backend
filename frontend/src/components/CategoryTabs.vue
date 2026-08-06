<template>
  <div class="category-tabs-wrapper">
    <div class="category-tabs" ref="tabsRef">
      <button v-for="cat in categories" :key="cat.id"
        :class="['cat-tab', { active: activeId === cat.id }]"
        @click="$emit('select', cat.id)">
        {{ cat.name }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({ categories: { type: Array, required: true }, activeId: { type: Number, required: true } })
defineEmits(["select"])
</script>

<style scoped>
.category-tabs-wrapper {
  position: sticky; top: var(--header-height); z-index: 50;
  background: var(--canvas); border-bottom: 1px solid var(--hairline);
  margin: 0 -24px; padding: 0 24px; margin-bottom: 24px;
}
.category-tabs {
  display: flex; gap: 24px; overflow-x: auto;
  -webkit-overflow-scrolling: touch; scrollbar-width: none;
}
.category-tabs::-webkit-scrollbar { display: none; }
.cat-tab {
  flex-shrink: 0; padding: 14px 2px;
  font-family: var(--font-mono); font-size: 12px; font-weight: 600; text-transform: uppercase;
  color: var(--text-muted); border-bottom: 2px solid transparent;
  transition: color 0.12s, border-color 0.12s; white-space: nowrap;
}
.cat-tab:hover { color: var(--mint); }
.cat-tab.active { color: var(--text); border-bottom-color: var(--mint); }
@media (max-width: 768px) { .category-tabs-wrapper { margin: 0 -16px; padding: 0 16px; } }
</style>
