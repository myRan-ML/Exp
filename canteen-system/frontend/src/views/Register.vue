<template>
  <div class="min-h-screen bg-cover bg-center flex items-center justify-center" style="background-image: url('/images/nuaa_canteen2.jpg')">
    <div class="bg-white bg-opacity-80 p-8 rounded-lg shadow-lg w-full max-w-md backdrop-blur-sm">
      <h2 class="text-3xl font-semibold text-center mb-6 text-gray-800">用户注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="mb-4">
          <label class="block text-gray-700 font-medium mb-1" for="username">用户名</label>
          <input v-model="username" id="username" type="text" class="w-full mt-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500" required />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 font-medium mb-1" for="password">密码</label>
          <input v-model="password" id="password" type="password" class="w-full mt-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500" required />
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 font-medium mb-1" for="role">角色</label>
          <select v-model="role" id="role" class="w-full mt-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500">
            <option value="customer">普通用户</option>
            <option value="admin">管理员</option>
          </select>
        </div>
        <button type="submit" class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition duration-200">注册</button>
      </form>
      <p class="mt-4 text-center text-sm text-gray-600">
        已有账号？
        <router-link to="/login" class="text-blue-600 hover:underline">登录</router-link>
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
    const role = ref('customer')
    const router = useRouter()

    const handleRegister = async () => {
      try {
        await axios.post('/api/user/register', { username: username.value, password: password.value, role: role.value })
        alert('注册成功，请登录')
        router.push('/login')
      } catch (err) {
        alert('注册失败，用户名可能已存在')
      }
    }

    return { username, password, role, handleRegister }
  }
})
</script>
