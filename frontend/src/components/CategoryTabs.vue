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
  background: var(--canvas); padding: 8px 0; margin: 0 -16px;
  padding-left: 16px; margin-bottom: 4px;
}
.category-tabs {
  display: flex; gap: 8px; overflow-x: auto;
  -webkit-overflow-scrolling: touch; scrollbar-width: none; padding-right: 16px;
}
.category-tabs::-webkit-scrollbar { display: none; }
.cat-tab {
  flex-shrink: 0; padding: 6px 16px; border-radius: var(--radius-pill);
  font-size: 14px; font-weight: 500; background: var(--surface);
  border: 1px solid var(--border); color: var(--text-secondary);
  transition: all 0.15s; white-space: nowrap;
}
.cat-tab:hover { border-color: var(--primary); color: var(--primary); }
.cat-tab.active { background: var(--primary); color: #fff; border-color: var(--primary); }
</style>
