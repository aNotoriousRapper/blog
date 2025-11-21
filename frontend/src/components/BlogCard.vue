<template>
  <div class="max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
    <a :href="`/post/${post.id}`">
      <img class="rounded-t-lg" :src="post.image" alt="" />
    </a>
    <div class="p-5">
      <a :href="`/post/${post.id}`">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{{ post.title }}</h5>
      </a>
      <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">{{ post.excerpt }}</p>
      <router-link :to="`/post/${post.id}`" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700">
        阅读更多
      </router-link>
    </div>
  </div>
</template>


<script setup>
defineProps({ post: Object })
</script>