<template>
  <div id="app-root">
    <AppHeader />
    <router-view />
  </div>
</template>

<script setup>
import AppHeader from '@/components/AppHeader.vue'
</script>

<style scoped>
#app-root {
  min-height: 100vh;
}
</style>
