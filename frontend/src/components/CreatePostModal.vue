<template>
  <div class="max-w-3xl mx-auto p-6 bg-white shadow-md rounded-xl">

    <h2 class="text-2xl font-bold mb-6 text-gray-800">发布帖子</h2>

    <!-- 标题 -->
    <label class="block mb-2 text-gray-700 font-semibold">标题</label>
    <input
        v-model="title"
        type="text"
        placeholder="请输入标题"
        class="w-full border rounded-lg px-4 py-2 mb-6 focus:ring focus:border-blue-400"
    />

    <!-- 内容 -->
    <label class="block mb-2 text-gray-700 font-semibold">内容</label>
    <textarea
        v-model="content"
        rows="6"
        placeholder="写下你的想法..."
        class="w-full border rounded-lg px-4 py-3 mb-6 focus:ring focus:border-blue-400"
    ></textarea>

    <!-- 标签选择 -->
    <label class="block mb-2 text-gray-700 font-semibold">标签</label>

    <div class="flex flex-wrap gap-2 mb-3">
      <span
          v-for="tag in availableTags"
          :key="tag"
          @click="toggleTag(tag)"
          :class="[
          'px-3 py-1 rounded-full border cursor-pointer text-sm',
          selectedTags.includes(tag)
            ? 'bg-blue-500 text-white'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        ]"
      >
        #{{ tag }}
      </span>
    </div>

    <!-- 自定义标签 -->
    <div class="flex gap-2 mb-6">
      <input
          v-model="newTag"
          type="text"
          placeholder="输入自定义标签并回车"
          @keyup.enter="addTag"
          class="flex-1 border rounded-lg px-4 py-2 focus:ring focus:border-blue-400"
      />
      <button
          @click="addTag"
          class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 whitespace-nowrap"
      >
        添加标签
      </button>
    </div>

    <!-- 已选标签显示 -->
    <div class="flex flex-wrap gap-2 mb-6">
      <span
          v-for="tag in selectedTags"
          :key="'sel-' + tag"
          class="px-3 py-1 bg-blue-500 text-white rounded-full flex items-center gap-2 text-sm"
      >
        #{{ tag }}
        <button
            @click="removeTag(tag)"
            class="w-5 h-5 flex items-center justify-center text-xs bg-white text-gray-700 rounded-full hover:bg-red-500 hover:text-white"
        >
        ✕
        </button>

      </span>
    </div>

    <!-- 发布按钮 -->
    <button
        @click="submitPost"
        class="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 w-full text-lg font-semibold"
    >
      发布
    </button>

  </div>
</template>

<script>
import axios from "axios";
import {useUserStore} from "../store/user.js";
import api from "../utils/api";

export default {
  data() {
    return {
      title: "",
      content: "",
      availableTags: ["随笔", "日常", "技术", "生活", "摄影", "编程", "学习"],
      selectedTags: [],
      newTag: "",
    };
  },

  methods: {
    toggleTag(tag) {
      if (this.selectedTags.includes(tag)) {
        this.selectedTags = this.selectedTags.filter(t => t !== tag);
      } else {
        this.selectedTags.push(tag);
      }
    },

    addTag() {
      if (!this.newTag.trim()) return;
      const tag = this.newTag.trim();

      if (!this.selectedTags.includes(tag)) {
        this.selectedTags.push(tag);
      }

      this.newTag = "";
    },

    removeTag(tag) {
      this.selectedTags = this.selectedTags.filter(t => t !== tag);
    },

    async submitPost() {
      if (!this.title || !this.content) {
        alert("标题和内容不能为空");
        return;
      }

      try {

        await api.post("/create", {
          title: this.title,
          content: this.content,
          tags: this.selectedTags
        });

        this.$emit("close"); // 关闭弹窗
        this.$emit("posted"); // 通知刷新
      } catch (err) {
        console.error(err);
      }
    }
  }
};
</script>
