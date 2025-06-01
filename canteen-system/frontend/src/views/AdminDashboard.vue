<template>
  <div :class="{'dark': isDarkMode}" class="min-h-screen bg-gradient-to-r from-blue-100 to-blue-50 dark:from-gray-800 dark:to-gray-900">
    <!-- 顶部导航栏 -->
    <nav class="bg-white dark:bg-gray-800 shadow-lg mb-8">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <img src="/images/logo.jpg" alt="南航食堂" class="w-10 h-10 rounded-full" />
          <span class="text-xl font-semibold text-gray-800 dark:text-white">管理员面板</span>
        </div>
        <div class="flex items-center space-x-4">
          <span class="text-gray-700 dark:text-gray-300">欢迎，{{ username }}</span>
          <button @click="toggleDarkMode" class="p-2 rounded-full bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600">
            <svg :class="{'text-yellow-500': !isDarkMode, 'text-gray-400': isDarkMode}" class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M11.293 3.293a1 1 0 011.414 0l4.5 4.5a1 1 0 010 1.414L14.707 9.707a1 1 0 01-1.414-1.414L15.793 5H13a5.978 5.978 0 00-3.21.88C8.503 4.35 7.026 3 5 3a5 5 0 115 5h2.586l-1.207 1.207a1 1 0 01-1.414-1.414L8.5 7.5a3.5 3.5 0 013.5-3.5c.892 0 1.732.333 2.36.84L14.707 5H13a1 1 0 01-1-1V2a5 5 0 115 5c-.775 0-1.5-.271-2.104-.707l1.23-1.23a1 1 0 00-.001-1.415z" clip-rule="evenodd"/>
            </svg>
          </button>
          <button @click="logout" class="bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600">退出登录</button>
        </div>
      </div>
    </nav>
    
    <!-- 管理员面板内容 -->
    <div class="max-w-5xl mx-auto">
      <h1 class="text-4xl font-bold text-gray-800 mb-8 text-center">欢迎进入管理员面板</h1>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link to="/admin/employees" class="admin-card">
          <UserIcon class="w-8 h-8 text-blue-600" />
          <span>员工管理</span>
        </router-link>
        <router-link to="/admin/dishes" class="admin-card">
          <UtensilsIcon class="w-8 h-8 text-green-600" />
          <span>菜品管理</span>
        </router-link>
        <router-link to="/admin/inventory" class="admin-card">
          <BoxesIcon class="w-8 h-8 text-yellow-600" />
          <span>库存管理</span>
        </router-link>
        <router-link to="/admin/report" class="admin-card">
          <BarChartIcon class="w-8 h-8 text-purple-600" />
          <span>订单报表</span>
        </router-link>
        <router-link to="/admin/window" class="admin-card">
          <LayoutIcon class="w-8 h-8 text-pink-600" />
          <span>窗口管理</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

// 图标来自 lucide (已安装即可用)
import { UserIcon, UtensilsIcon, BoxesIcon, BarChartIcon, LayoutIcon } from 'lucide-vue-next'

export default defineComponent({
  name: 'AdminDashboard',
  components: { UserIcon, UtensilsIcon, BoxesIcon, BarChartIcon, LayoutIcon },
  setup() {
    const router = useRouter()
    const username = ref(localStorage.getItem('username') || '管理员')
    const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')

    // 切换夜间模式
    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', String(isDarkMode.value))
    }

    // 退出登录
    const logout = () => {
      localStorage.removeItem('role')
      localStorage.removeItem('uid')
      localStorage.removeItem('username')
      router.push('/login')
    }

    onMounted(() => {
      const role = localStorage.getItem('role')
      if (role !== 'admin') {
        alert('您无权访问此页面')
        router.push('/login')
      }
    })
    
    return { username, isDarkMode, toggleDarkMode, logout }
  }
})
</script>

<style scoped>
.admin-card {
  @apply bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition duration-300 flex flex-col items-center justify-center space-y-3 text-lg font-medium text-gray-700 hover:scale-105 cursor-pointer;
}

nav {
  position: sticky;
  top: 0;
  z-index: 10;
}
</style>
