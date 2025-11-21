<template>
  <div class="min-h-screen flex flex-col bg-gray-50 text-gray-800">

    <!-- 页面主体内容 -->
    <main class="flex-1 container mx-auto px-4 py-6">
      <!-- 导航栏 -->
      <RouterView />
    </main>

    <!-- 页脚 -->
    <Footer />
  </div>
</template>

<script setup>
import Footer from './components/Footer.vue'
</script>

<style>
/* 让页面背景更柔和 */
body {
  background-color: #f9fafb;
}
</style>
