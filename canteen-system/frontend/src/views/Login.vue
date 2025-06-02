<template>
  <div class="min-h-screen bg-cover bg-center flex items-center justify-center" style="background-image: url('/images/nuaa_canteen1.jpg')">
    <div class="bg-white bg-opacity-80 p-8 rounded-lg shadow-lg w-full max-w-md backdrop-blur-sm">
      
      <!-- 标题与校徽、食堂标志、个人头像 -->
      <div class="flex items-center justify-between mb-6">
        <!-- 南航校徽 -->
        <img src="/images/nuaa_logo.jpg" alt="南航校徽" class="h-12" />
        <!-- 个人头像 -->
        <img src="/images/avatar.jpg" alt="个人头像" class="h-12 rounded-full border-2 border-blue-600" />
        <!-- 南航食堂标志 -->
        <img src="/images/canteen_logo.jpg" alt="食堂标志" class="h-12" />
      </div>

      <!-- 南航及智慧食堂系统标题 -->
      <h2 class="text-3xl font-semibold text-center mb-6 text-gray-800">
        南京航空航天大学
        <br />
        智慧食堂系统
      </h2>

      <!-- 欢迎登录文本 -->
      <h2 class="text-3xl font-semibold text-center mb-6 text-gray-800">欢迎登录</h2>

      <!-- 登录表单 -->
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-gray-700 font-medium mb-1" for="username">用户名</label>
          <input v-model="username" id="username" type="text" class="w-full mt-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" required />
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 font-medium mb-1" for="password">密码</label>
          <input v-model="password" id="password" type="password" class="w-full mt-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" required />
        </div>
        <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition duration-200">登录</button>
      </form>

      <!-- 注册链接 -->
      <p class="mt-4 text-center text-sm text-gray-600">
        没有账号？
        <router-link to="/register" class="text-blue-600 hover:underline">注册</router-link>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    const username = ref('')
    const password = ref('')
    const router = useRouter()

    const handleLogin = async () => {
      try {
        const res = await axios.post('/api/user/login', {
          username: username.value,
          password: password.value
        })
        const role = res.data.role
        localStorage.setItem('role', role)
        localStorage.setItem("uid", res.data.uid)
        if (role === 'admin') {
          router.push('/admin')
        } else {
          router.push('/customer')
        }
      } catch (err) {
        alert('登录失败，请检查用户名或密码')
      }
    }

    return { username, password, handleLogin }
  }
})
</script>

<style scoped>
/* 背景和容器的样式 */
.min-h-screen {
  background-image: url('/images/nuaa_canteen1.jpg');
  background-size: cover;
  background-position: center;
}

/* 表单容器样式 */
.bg-white {
  background-color: rgba(255, 255, 255, 0.8); /* 半透明白色背景 */
}

.backdrop-blur-sm {
  backdrop-filter: blur(5px);
}

/* 校徽、食堂标志和头像的样式 */
img {
  object-fit: contain;
}

/* 头像的样式 */
img.rounded-full {
  border: 2px solid #3b82f6;
}

/* 按钮和输入框的样式 */
button {
  transition: all 0.3s ease;
}

input[type="text"], input[type="password"] {
  font-size: 1rem;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: #f9fafb;
  transition: all 0.3s ease;
}

input[type="text"]:focus, input[type="password"]:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .flex {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
