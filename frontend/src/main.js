import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import 'flowbite'
import './style.css'
import axios from 'axios'

const app = createApp(App)

// 设置全局后端 API 基础路径
axios.defaults.baseURL = 'http://localhost:5000'
app.config.globalProperties.$axios = axios



const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(pinia);

app.use(router)
app.mount('#app')
