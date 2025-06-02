<template>
  <div class="bg-white p-6 rounded shadow">
    <h2 class="text-2xl font-semibold mb-4">🍽️ 菜品列表</h2>
    <input
      type="text"
      v-model="searchQuery"
      placeholder="搜索菜品..."
      class="w-full p-2 border rounded-lg mb-4"
    />
    <div v-if="filteredDishes.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="dish in filteredDishes"
        :key="dish.DNO"
        class="bg-gray-50 p-4 rounded-lg shadow hover:shadow-md transition"
      >
        <!-- 菜品图片 -->
        <div class="w-full h-40 overflow-hidden mb-4">
          <img 
            v-if="dish.DIMAGE" 
            :src="dish.DIMAGE" 
            alt="菜品图片" 
            class="w-full h-full object-cover rounded"
          />
        </div>
        <h3 class="text-lg font-bold text-gray-800">{{ dish.DNAME }}</h3>
        <p class="mt-1 text-sm text-gray-600">价格: ¥{{ dish.DPRICE }}</p>
        <!-- 修改为 "剩余" 显示 -->
        <p class="mt-1 text-sm text-gray-600">剩余: {{ dish.STOCK }} 份</p>
        <div class="mt-3 flex items-center">
          <input
            type="number"
            v-model.number="quantities[dish.DNO]"
            min="1"
            :max="dish.STOCK"
            class="w-20 p-1 border rounded mr-2"
          />
          <button
            @click="addDishToCart(dish)"
            :disabled="!quantities[dish.DNO] || quantities[dish.DNO] > dish.STOCK"
            class="bg-blue-500 text-white py-1 px-3 rounded hover:bg-blue-600 disabled:opacity-50"
          >
            加入购物车
          </button>
        </div>
      </div>
    </div>
    <div v-else class="text-gray-500">暂无菜品。</div>

    <!-- 提示框 -->
    <div v-if="showAddToCartMessage" class="fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded shadow-lg z-50">
      {{ addToCartMessage }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, computed, onMounted } from 'vue'
import axios from 'axios'

// 定义菜品的类型
interface Dish {
  DNO: string
  DNAME: string
  DPRICE: number
  STOCK: number
  DIMAGE: string | null  // 确保字段名与后端一致
}

export default defineComponent({
  name: 'DishList',
  emits: ['add-to-cart'],
  setup(_, { emit }) {
    const dishes = ref<Dish[]>([])
    const quantities = reactive<Record<string, number>>({})
    const searchQuery = ref('')
    const showAddToCartMessage = ref(false)
    const addToCartMessage = ref('')
    
    // 获取菜品数据
    const fetchDishes = async () => {
      try {
        const res = await axios.get('/api/dish/all')
        dishes.value = res.data
        dishes.value.forEach((d) => {
          quantities[d.DNO] = 1
        })
      } catch (err) {
        console.error('获取菜品失败：', err)
      }
    }

    onMounted(fetchDishes)

    // 过滤菜品数据
    const filteredDishes = computed(() => {
      return dishes.value.filter((dish) =>
        dish.DNAME.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    // 加入购物车逻辑
    const addDishToCart = (dish: Dish) => {
      emit('add-to-cart', { dish, quantity: quantities[dish.DNO] })
      addToCartMessage.value = `${dish.DNAME} 已成功加入购物车！`
      showAddToCartMessage.value = true
      setTimeout(() => {
        showAddToCartMessage.value = false
      }, 2000)
    }

    return {
      dishes,
      quantities,
      searchQuery,
      filteredDishes,
      showAddToCartMessage,
      addToCartMessage,
      addDishToCart
    }
  }
})
</script>

<style scoped>
/* 提示框动画 */
.fixed {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  z-index: 999;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

/* 响应式图片 */
img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

/* 按钮和输入框 */
input[type="number"] {
  border-radius: 8px;
  border: 1px solid #ddd;
}

button {
  transition: background-color 0.2s ease;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
