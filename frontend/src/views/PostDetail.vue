<template>
  <div class="bg-gray-50 min-h-screen">
    <Navbar />

    <!-- 页面主体 -->
    <div class="max-w-7xl mx-auto px-8 pt-28 grid grid-cols-12 gap-8">

      <!-- 主体内容区 -->
      <div class="col-span-12 lg:col-span-8 bg-white shadow-sm rounded-2xl p-10">
        <h1 class="text-4xl font-bold mb-6 leading-snug">{{ post.title }}</h1>

        <div class="flex items-center gap-3 text-gray-500 text-sm mb-10">
          <img src="https://i.pravatar.cc/40" class="rounded-full w-8 h-8" alt="author" />
          <span>{{ post.author }}</span>
          <span>·</span>
          <span>{{ post.date }}</span>
        </div>

        <div class="prose max-w-none text-gray-800 leading-relaxed text-lg mb-16">
          <p class="mb-6">{{ post.content }}</p>
          <!-- 标签区域 -->
          <div class="flex flex-wrap justify-end gap-2 mt-4">
            <span
              v-for="tag in post.tags"
              :key="tag"
              class="px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded-full border"
            >
              #{{ tag }}
            </span>
          </div>
        </div>

        <!-- 评论区 -->
        <div class="border-t pt-8">
          <h2 class="text-2xl font-semibold mb-6">💬 评论区</h2>

          <!-- 评论列表 -->
          <div v-if="comments.length" class="space-y-6 mb-10">
            <div
                v-for="comment in comments"
                :key="comment.id"
                class="bg-gray-100 rounded-xl p-4 border border-gray-200"
            >
              <div class="flex items-center gap-3 mb-2">
                <img src="https://i.pravatar.cc/35?u={{comment.username}}" class="rounded-full" alt="" />
                <p class="font-semibold text-gray-900">{{ comment.username }}</p>
                <span class="text-xs text-gray-500">{{ formatDate(comment.created_at) }}</span>
              </div>

              <!-- 内容 + 删除按钮 -->
              <div class="flex justify-between items-end">
                <p class="text-gray-700 ml-12 text-left">{{ comment.content }}</p>

                <!-- 删除按钮 -->
                <button
                    v-if="userStore.user_id == comment.user_id"
                    @click="deleteComment(comment.id)"
                    class="text-red-500 text-sm underline hover:text-red-700 ml-4 whitespace-nowrap"
                >
                  删除
                </button>

              </div>
            </div>
          </div>

          <p v-else class="text-gray-500 mb-8">暂无评论，快来抢沙发吧！</p>

          <!-- 发布评论 -->
          <div class="bg-gray-50 border border-gray-200 rounded-xl p-6">
            <h3 class="text-lg font-semibold mb-3">发表评论</h3>
            <textarea
                v-model="newComment"
                placeholder="写下你的评论..."
                class="w-full border rounded-lg p-3 h-24 resize-none focus:ring-2 focus:ring-blue-500 mb-3"
            ></textarea>
            <button
                @click="addComment"
                class="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              发布
            </button>
          </div>
        </div>
      </div>

      <!-- 侧边栏 -->
      <aside class="hidden lg:block col-span-4 space-y-8">
        <!-- 作者卡片 -->
        <div class="bg-white shadow-sm rounded-2xl p-6">
          <div class="flex items-center gap-4 mb-4">
            <img src="https://i.pravatar.cc/60" class="rounded-full" />
            <div>
              <p class="font-semibold text-lg">{{ post.author }}</p>
              <p class="text-gray-500 text-sm">技术博主 / 全栈开发者</p>
            </div>
          </div>
          <p class="text-gray-600 text-sm leading-relaxed">
            热爱 Web 开发与数据分析，专注于 Vue、Flask、Python 全栈方向。
          </p>
        </div>

        <!-- 推荐文章 -->
        <div class="bg-white shadow-sm rounded-2xl p-6">
          <h3 class="text-xl font-semibold mb-4">🔥 推荐阅读</h3>
          <ul class="space-y-3">
            <li
                v-for="(rec, index) in recommended"
                :key="index"
                class="border-b pb-2 last:border-0"
            >
              <router-link
                  :to="`/post/${rec.id}`"
                  class="text-blue-600 hover:text-blue-800 font-medium"
              >
                {{ rec.title }}
              </router-link>
              <p class="text-gray-500 text-sm">{{ rec.date }}</p>
            </li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import {onMounted, ref} from 'vue'
import axios from "axios";
import router from "../router/index.js";
import { useUserStore } from '../store/user'
import api from "../utils/api.js";

const resJson = ref([])
const post = ref([])
const loading = ref(true)
const comments = ref([])
const newComment = ref('')
const error = ref("");
const userStore = useUserStore()
const recommended = [
  { id: 2, title: '使用 Tailwind 优化 Vue 界面', date: '2025-10-20' },
  { id: 3, title: 'Flask API 接口设计规范', date: '2025-09-15' },
  { id: 4, title: 'Pinia 状态管理最佳实践', date: '2025-09-02' },
]

onMounted(() => {
  loadDetails()
})

const loadDetails = async () => {
  // 停止执行 2 秒钟
  try {
    const res = await fetch('http://127.0.0.1:5000' + window.location.pathname)
    if (!res.ok) throw new Error('网络错误')
    resJson.value = await res.json()
    post.value.author = resJson.value.author
    post.value.title = resJson.value.title
    post.value.content = resJson.value.content
    post.value.tags = resJson.value.tags
    comments.value = resJson.value.comments
    console.log(comments.value)
  } catch (err) {
    console.error('加载博客失败：', err)
  } finally {
    loading.value = false
  }
}

const addComment = async () => {
  const res = await api.post( window.location.pathname + "/comments", {
    newComment: newComment.value,
  });

  if (res.status === 200) {
    console.log('评论发布成功')
    await loadDetails()
  }
};

const deleteComment = async (id) => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/comment/'+id+'/delete', {});
    if (res.status === 200) {
      console.log('删除评论成功')
    }
  } catch (err) {
    console.log(err)
  } finally {
    loadDetails()
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
</script>

<style scoped>
.prose p {
  margin-bottom: 1.5rem;
  line-height: 1.8;
}
</style>
