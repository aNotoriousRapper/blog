<template>
  <div>
    <Navbar />
    <div class="flex justify-center items-center min-h-screen bg-gray-50 pt-20">
      <div class="w-full max-w-md bg-white shadow-lg p-10 rounded-2xl">
        <h2 class="text-3xl font-semibold text-center mb-8">注册</h2>
        <p v-if="error" class="error-message">{{ error }}</p>
        <br>
        <form @submit.prevent="register" class="space-y-6">
          <input v-model="email" type="text" placeholder="邮箱账号" class="w-full border rounded-lg px-4 py-3" />
          <input v-model="username" type="text" placeholder="用户名" class="w-full border rounded-lg px-4 py-3" />
          <input v-model="password" type="password" placeholder="密码" class="w-full border rounded-lg px-4 py-3" />
          <input v-model="confirm_password" type="password" placeholder="重复密码" class="w-full border rounded-lg px-4 py-3" />
          <button type="submit" class="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition">注册</button>
        </form>
        <p class="text-center mt-6 text-gray-600">
          已有账号？
          <router-link to="/login" class="text-blue-600 hover:underline">登录</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import { useRouter } from 'vue-router'
import axios from "axios";
import {ref} from "vue";

const router = useRouter()
const email = ref("");
const username = ref("");
const password = ref("");
const confirm_password = ref("");
const error = ref("");


const register = async () => {
  try {
    const res = await axios.post("/register", {
      email: email.value,
      username: username.value,
      password: password.value,
      confirm_password: confirm_password.value,
    });

    if (res.status === 200) {
      router.push("/login");
    }
  } catch (err) {
    error.value = err.response.data.message;
    router.push("/register");
  }
};
</script>
