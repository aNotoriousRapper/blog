<template>
  <div>
    <Navbar @open-create="showCreateModal = true" />
    <div class="max-w-6xl mx-auto px-8 pt-24">
      <h1 class="text-4xl font-bold mb-8">最新博客</h1>

      <!-- 新增：真正的双栏布局容器 -->
      <div class="flex gap-10 items-start">

        <!-- 左侧：文章列表（自动占满剩余空间） -->
        <div class="flex-1">

          <div v-if="loading" class="text-gray-500 text-lg">加载中...</div>
          <div v-else-if="posts.length === 0" class="text-gray-500 text-lg">暂无博客内容</div>

          <div
              v-else
              v-for="post in posts"
              :key="post.id"
              class="mb-10 border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition p-6"
          >
            <router-link :to="`/post/${post.id}`" class="text-2xl text-blue-600 hover:underline font-semibold">
              {{ post.title }}
            </router-link>

            <p class="text-gray-500 mt-2 text-sm">
              作者: {{ post.author }} | 发布时间: {{ formatDate(post.created_at) }}
            </p>

            <p class="text-gray-600 mt-3 text-lg leading-relaxed">{{ post.content }}</p>
          </div>
          <!-- 分页按钮 -->
          <div class="flex justify-center items-center mt-8 gap-4" v-if="totalPages > 1">
            <!-- 上一页 -->
            <button
                @click="prevPage"
                :disabled="page === 1"
                class="px-4 py-2 rounded-lg border bg-white hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              上一页
            </button>

            <span class="text-gray-700">第 {{ page }} / {{ totalPages }} 页</span>

            <!-- 下一页 -->
            <button
                @click="nextPage"
                :disabled="page === totalPages"
                class="px-4 py-2 rounded-lg border bg-white hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              下一页
            </button>
          </div>

        </div>

        <!-- 右侧：排行榜（固定宽度） -->
        <div class="w-80 sticky top-28">
          <div class="border border-gray-200 rounded-xl p-5 bg-white shadow-sm">
            <h2 class="text-xl font-semibold mb-4">🔥 文章排行榜</h2>

            <div v-if="rankings.length === 0" class="text-gray-500">暂无数据</div>

            <ul v-else class="space-y-3">
              <li v-for="(item, index) in rankings" :key="item.id" class="flex justify-between items-center">
                <router-link :to="`/post/${item.id}`" class="text-blue-600 hover:underline text-sm truncate w-40">
                  {{ index + 1 }}. {{ item.title }}
                </router-link>
                <span class="text-gray-500 text-xs">{{ item.views }} 浏览</span>
              </li>
            </ul>
          </div>
        </div>

  </div>

      <!-- 弹窗 -->
      <transition name="fade">
        <div
            v-if="showCreateModal"
            class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
        >
          <div class="bg-white rounded-xl shadow-lg w-full max-w-3xl p-6 relative">

            <button
                @click="showCreateModal = false"
                class="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-200"
            >
              ✕
            </button>

            <CreatePostModal @close="showCreateModal = false" @posted="fetchPosts" />
          </div>
        </div>
      </transition>

    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import CreatePostModal from "../components/CreatePostModal.vue"

const posts = ref([])
const rankings = ref([])  // 👉 新增排行榜数据
const loading = ref(true)
const showCreateModal = ref(false)
// 分页
const page = ref(1)
const perPage = 10
const totalPages = ref(1)

onMounted(() => {
  fetchPosts()
  fetchRankings()
})

const fetchPosts = async () => {
  await new Promise(resolve => setTimeout(resolve, 500))
  try {
    const res = await fetch(`http://127.0.0.1:5000/posts?page=${page.value}&per_page=${perPage}`)
    if (!res.ok) throw new Error('网络错误')
    const data = await res.json()
    console.log(data)
    console.log(data.post)
    posts.value = data.posts
    totalPages.value = data.pages
  } catch (err) {
    console.error('加载博客失败：', err)
  } finally {
    loading.value = false
  }
}

// 👉 新增排行榜 API
const fetchRankings = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/posts/rank')
    if (!res.ok) throw new Error('网络错误')
    rankings.value = await res.json()
  } catch (err) {
    console.error('加载排行榜失败：', err)
  }
}

function formatDate(datetime) {
  const d = new Date(datetime)
  const month = d.getMonth() + 1
  const day = d.getDate()
  const hour = d.getHours()
  const minute = d.getMinutes()
  return `${month}月${day}日 ${hour}:${minute.toString().padStart(2, '0')}`
}

const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++
    fetchPosts()
  }
}

const prevPage = () => {
  if (page.value > 1) {
    page.value--
    fetchPosts()
  }
}

</script>


<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
