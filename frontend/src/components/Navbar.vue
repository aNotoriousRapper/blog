<template>
  <nav class="bg-white border-b border-gray-200 shadow-sm fixed w-full top-0 left-0 z-50">
    <div class="max-w-7xl mx-auto px-8 py-3 flex justify-between items-center">
      <router-link to="/" class="text-2xl font-semibold text-blue-600 hover:text-blue-700">WolfBlog</router-link>

      <div>
        <template v-if="userStore.isLoggedIn">

          <span class="mr-6 text-gray-700 text-lg">你好，{{ userStore.username }}</span>
          <!-- 发布按钮 -->
          <button @click="$emit('open-create')" class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600">发布</button>
          <button @click="logout" class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 ml-3">注销</button>
        </template>
        <template v-else>
          <router-link to="/login" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">登录</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useUserStore } from '../store/user'
const userStore = useUserStore()

function logout() {
  userStore.logout()
}

</script>
