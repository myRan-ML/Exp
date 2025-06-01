<template>
  <div class="bg-white p-6 rounded shadow">
    <h2 class="text-2xl font-semibold mb-4">🍽️ 菜品列表</h2>
    <div v-if="dishes.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="dish in dishes"
        :key="dish.DNO"
        class="bg-gray-50 p-4 rounded-lg shadow hover:shadow-md transition"
      >
        <h3 class="text-lg font-bold text-gray-800">{{ dish.DNAME }}</h3>
        <p class="mt-1 text-sm text-gray-600">价格: ¥{{ dish.DPRICE }}</p>
        <p class="mt-1 text-sm text-gray-600">库存: {{ dish.STOCK }}</p>
        <div class="mt-3 flex items-center">
          <input
            type="number"
            v-model.number="quantities[dish.DNO]"
            min="1"
            :max="dish.STOCK"
            class="w-20 p-1 border rounded mr-2"
          />
          <button
            @click="$emit('add-to-cart', { dish, quantity: quantities[dish.DNO] })"
            :disabled="!quantities[dish.DNO] || quantities[dish.DNO] > dish.STOCK"
            class="bg-blue-500 text-white py-1 px-3 rounded hover:bg-blue-600 disabled:opacity-50"
          >
            加入购物车
          </button>
        </div>
      </div>
    </div>
    <div v-else class="text-gray-500">暂无菜品。</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from 'vue'
import axios from 'axios'

interface Dish {
  DNO: string
  DNAME: string
  DPRICE: number
  STOCK: number
}

export default defineComponent({
  name: 'DishList',
  emits: ['add-to-cart'],
  setup(_, { emit }) {
    const dishes = ref<Dish[]>([])
    const quantities = reactive<Record<string, number>>({})

    const fetchDishes = async () => {
      try {
      const res = await axios.get('/api/dish/all')
      console.log('返回菜品数据：', res.data)  // ✅ 看一下控制台输出
      dishes.value = res.data
      dishes.value.forEach((d) => {
        quantities[d.DNO] = 1
      })
    } catch (err) {
      console.error('获取菜品失败：', err)
    }
  }

    onMounted(fetchDishes)

    return {
      dishes,
      quantities
    }
  }
})
</script>
