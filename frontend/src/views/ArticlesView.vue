<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const articles = ref([]);

onMounted(async () => {
  const response = await api.get("/articles");
  articles.value = response.data;
});
</script>

<template>
  <div>
    <h1>Articles</h1>

    <div
      v-for="article in articles"
      :key="article.article_id"
    >
      {{ article.title }}
    </div>
  </div>
</template>