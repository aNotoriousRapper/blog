// src/utils/api.js
import axios from "axios";
import { useUserStore } from "../store/user.js";

const api = axios.create({
    baseURL: "http://localhost:5000",
    withCredentials: true  // 🔥 必须，让浏览器自动带上 refresh_token cookie
});

// ======================
// REQUEST 拦截器
// ======================
api.interceptors.request.use(
    (config) => {
        config.headers["Content-Type"] = "application/json";
        const userStore = useUserStore();
        console.log(userStore.access_token);
        if (userStore.access_token) {
            config.headers.Authorization = `Bearer ${userStore.access_token}`;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// ======================
// RESPONSE 拦截器（自动刷新 Access Token）
// ======================

let isRefreshing = false;
let requestsQueue = [];

function subscribeTokenRefresh(cb) {
    requestsQueue.push(cb);
}

function onTokenRefreshed(newToken) {
    requestsQueue.forEach((cb) => cb(newToken));
    requestsQueue = [];
}

api.interceptors.response.use(
    (response) => response,

    async (error) => {
        const { response, config } = error;
        const userStore = useUserStore();
        console.log(userStore.access_token);
        // 不是 401 → 直接报错
        if (!response || response.status !== 401 || config._retry) {
            return Promise.reject(error);
        }

        config._retry = true;

        // ======================
        // 第一次遇到 401 → 发 refresh 请求
        // ======================
        if (!isRefreshing) {
            isRefreshing = true;

            try {
                const res = await api.post("/api/refresh");
                const newToken = res.data.access_token;

                userStore.setAccessToken(newToken);

                // 通知所有等待中的请求
                onTokenRefreshed(newToken);
                isRefreshing = false;

            } catch (refreshErr) {
                isRefreshing = false;
                userStore.logout();
                return Promise.reject(refreshErr);
            }
        }

        // ======================
        // 其他请求等待新 token
        // ======================
        return new Promise((resolve) => {
            subscribeTokenRefresh((newToken) => {
                config.headers.Authorization = `Bearer ${newToken}`;
                resolve(api(config));
            });
        });
    }
);

export default api;
