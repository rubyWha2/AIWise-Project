<script setup lang="ts">
</script>

<template>
  <div class="min-h-screen bg-white text-zinc-900 antialiased">
    <router-view />
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
