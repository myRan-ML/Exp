<template>
  <div class="min-h-screen bg-cover bg-center bg-gray-100" style="background-image: url('/images/cafeteria.jpg');">
    <!-- 顶部导航 -->
    <header class="bg-white bg-opacity-70 shadow p-4 flex justify-between items-center">
      <h1 class="text-2xl font-bold">南航食堂系统</h1>
      <div class="flex items-center gap-4">
        <button
          v-if="role === 'admin'"
          @click="goToAdmin"
          class="bg-yellow-500 text-white px-4 py-1 rounded hover:bg-yellow-600"
        >
          管理员后台
        </button>
        <button
          @click="goToOrderHistory"
          class="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600"
        >
          查看订单
        </button>
        <button
          @click="logout"
          class="bg-red-500 text-white px-4 py-1 rounded hover:bg-red-600"
        >
          退出登录
        </button>
      </div>
    </header>

    <!-- 主体 -->
    <div class="max-w-7xl mx-auto mt-6 grid grid-cols-3 gap-6">
      <div class="col-span-2 bg-white bg-opacity-70 p-4 rounded-lg shadow-lg">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索菜品..."
          class="w-full p-2 border rounded-lg mb-4"
        />
        <DishList 
          @add-to-cart="addToCart" 
          :search-query="searchQuery"
        />
      </div>
      <div class="bg-white bg-opacity-70 p-4 rounded-lg shadow-lg">
        <OrderForm
          :cart-items="cartItems"
          :remove-from-cart="removeFromCart"
          @order-success="handleOrderSuccess"
          @order-failed="handleOrderFailed"
        />
      </div>
    </div>

    <!-- 成功提示 -->
    <div
      v-if="message"
      class="fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded shadow-lg z-50"
    >
      {{ message }}
    </div>

    <!-- 错误提示 -->
    <div
      v-if="errorMessage"
      class="fixed bottom-4 right-4 bg-red-500 text-white px-4 py-2 rounded shadow-lg z-50"
    >
      {{ errorMessage }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import DishList from '../components/DishList.vue'
import OrderForm from '../components/OrderForm.vue'

export default defineComponent({
  name: 'CustomerDashboard',
  components: {
    DishList,
    OrderForm
  },
  setup() {
    const cartItems = ref<any[]>([])
    const message = ref('')
    const errorMessage = ref('')
    const router = useRouter()
    const role = localStorage.getItem('role') || ''
    const searchQuery = ref('')

    const addToCart = ({ dish, quantity }: { dish: any; quantity: number }) => {
      const existing = cartItems.value.find((item) => item.DNO === dish.DNO)
      if (existing) {
        existing.quantity += quantity
      } else {
        cartItems.value.push({
          DNO: dish.DNO,
          DNAME: dish.DNAME,
          quantity
        })
      }
    }

    const removeFromCart = (dno: string) => {
      cartItems.value = cartItems.value.filter((item) => item.DNO !== dno)
    }

    const logout = () => {
      localStorage.clear()
      router.push('/login')
    }

    const goToAdmin = () => {
      router.push('/admin')
    }

    const goToOrderHistory = () => {
      router.push('/order-history')
    }

    // 下单成功处理
    const handleOrderSuccess = (msg: string) => {
      cartItems.value = []
      message.value = msg
      setTimeout(() => {
        message.value = ''
      }, 3000)
    }

    // 下单失败处理
    const handleOrderFailed = (msg: string) => {
      errorMessage.value = msg
      setTimeout(() => {
        errorMessage.value = ''
      }, 3000)
    }

    return {
      cartItems,
      addToCart,
      removeFromCart,
      logout,
      goToAdmin,
      goToOrderHistory,
      handleOrderSuccess,
      handleOrderFailed,
      message,
      errorMessage,
      role,
      searchQuery
    }
  }
})
</script>

<style scoped>
.min-h-screen {
  background-image: url('/images/cafeteria.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed; /* 改进背景图的效果 */
}

header {
  background-color: rgba(255, 255, 255, 0.7); /* 设置背景透明度 */
}

button {
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.bg-opacity-70 {
  background-color: rgba(255, 255, 255, 0.7); /* 菜单列表和购物车的透明度 */
}

input[type="text"] {
  font-size: 1rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  transition: all 0.3s ease;
}

input[type="text"]:focus {
  border-color: #1d4ed8;
  outline: none;
}

input[type="text"]::placeholder {
  color: #6b7280;
}
</style>
