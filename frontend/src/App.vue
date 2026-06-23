<script setup lang="ts">
import ArticlesView from './views/ArticlesView.vue'
</script>

<template>
<div class="min-h-screen bg-white text-zinc-900 antialiased">
    <ArticlesView />
    <!-- Routed views render inside the main content area -->
    <main class="pt-16">

    </main>
    <ToastContainer />
  </div>
</template>

<style>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>