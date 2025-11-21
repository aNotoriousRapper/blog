<template>
  <div>
    <Navbar />
    <div class="flex justify-center items-center min-h-screen bg-gray-50 pt-20">
      <div class="w-full max-w-md bg-white shadow-lg p-10 rounded-2xl">
        <h2 class="text-3xl font-semibold text-center mb-8">登录</h2>
        <!-- 👇 错误提示信息（只有有内容时才显示） -->
        <p v-if="error" class="error-message">{{ error }}</p>
        <br>
        <form @submit.prevent="login" class="space-y-6">
          <input v-model="email" type="text" placeholder="邮箱" class="w-full border rounded-lg px-4 py-3" />
          <input v-model="password" type="password" placeholder="密码" class="w-full border rounded-lg px-4 py-3" />
          <button type="submit" class="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition">登录</button>
        </form>
        <p class="text-center mt-6 text-gray-600">
          还没有账号？
          <router-link to="/register" class="text-blue-600 hover:underline">注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useUserStore } from '../store/user'
import Navbar from "../components/Navbar.vue";

const router = useRouter();
const email = ref("");
const password = ref("");
const error = ref("");
const userStore = useUserStore()

const login = async () => {
  try {
    const res = await axios.post("/api/login", {
      email: email.value,
      password: password.value,
    });

    if (res.status === 200) {
      userStore.login(res.data.username, res.data.user_id, res.data.access_token)
      const path = localStorage.getItem("origin_path");
      if (path) {
        localStorage.removeItem("origin_path")
        router.push(path)
      }else{
        router.push("/");
      }
    }

  } catch (err) {
    error.value = err.response.data.message;
    router.push("/login");
  }
};
</script>

