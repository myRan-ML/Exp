<template>
  <div class="min-h-screen bg-cover bg-center flex items-center justify-center" style="background-image: url('/images/nuaa_canteen1.jpg')">
    <div class="bg-white bg-opacity-80 p-8 rounded-lg shadow-lg w-full max-w-md backdrop-blur-sm">
      <h2 class="text-3xl font-semibold text-center mb-6 text-gray-800">欢迎登录</h2>
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
