<template>
  <div class="p-6">
    <h2 class="text-2xl font-semibold mb-4">🍲 菜品管理</h2>
    
    <!-- 添加菜品表单 -->
    <form @submit.prevent="addDish" class="mb-6 flex flex-col gap-4 bg-white p-6 rounded-lg shadow-md">
      <input v-model="newDish.DNO" placeholder="编号" class="border p-2 rounded" />
      <input v-model="newDish.DNAME" placeholder="名称" class="border p-2 rounded" />
      <input v-model="newDish.DPRICE" placeholder="价格" type="number" class="border p-2 rounded" />
      <input v-model="newDish.DIMAGE" placeholder="图片 URL" class="border p-2 rounded" />
      
      <button class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition">
        添加菜品
      </button>
    </form>

    <!-- 菜品列表 -->
    <ul class="space-y-2">
      <li v-for="dish in dishes" :key="dish.DNO" class="p-4 border rounded bg-gray-50 flex justify-between items-center">
        
        <!-- 显示菜品图片 -->
        <div class="flex items-center gap-4">
          <img v-if="dish.DIMAGE" :src="dish.DIMAGE" alt="菜品图片" class="w-20 h-20 object-cover rounded" />
          <span class="font-bold text-lg">{{ dish.DNAME }}</span>
        </div>
        
        <span class="text-sm text-gray-600">¥{{ dish.DPRICE }}</span>

        <!-- 修改价格按钮 -->
        <button 
          @click="editPrice(dish.DNO)" 
          class="text-blue-500 hover:underline ml-2">
          修改价格
        </button>
        
        <!-- 修改价格输入框 -->
        <div v-if="editingDish === dish.DNO" class="flex items-center gap-2">
          <input 
            v-model="newPrice" 
            type="number" 
            placeholder="新价格" 
            class="border p-2 rounded w-24"
          />
          <button 
            @click="updatePrice(dish.DNO)" 
            class="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600">
            更新
          </button>
          <button 
            @click="cancelEdit" 
            class="text-gray-500 hover:underline">
            取消
          </button>
        </div>

        <!-- 删除按钮 -->
        <button @click="removeDish(dish.DNO)" class="text-red-500 hover:underline ml-4">
          删除
        </button>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'

interface Dish {
  DNO: string
  DNAME: string
  DPRICE: number
  DIMAGE: string | null
}

export default defineComponent({
  setup() {
    const dishes = ref<Dish[]>([])
    const newDish = ref<Dish>({ DNO: '', DNAME: '', DPRICE: 0, DIMAGE: '' })
    const editingDish = ref<string | null>(null) // 当前正在编辑价格的菜品
    const newPrice = ref<number | null>(null) // 输入的新价格

    const load = async () => {
      const res = await axios.get('/api/dish/all')
      dishes.value = res.data
    }

    const addDish = async () => {
      if (!newDish.value.DNO || !newDish.value.DNAME || !newDish.value.DPRICE || !newDish.value.DIMAGE) {
        alert("请填写完整的菜品信息")
        return
      }
      await axios.post('/api/dish/add', newDish.value)
      newDish.value = { DNO: '', DNAME: '', DPRICE: 0, DIMAGE: '' }
      await load()
    }

    const removeDish = async (dno: string) => {
      await axios.delete(`/api/dish/delete/${dno}`)
      await load()
    }

    // 编辑价格功能
    const editPrice = (dno: string) => {
      editingDish.value = dno // 设置当前编辑的菜品
      const dish = dishes.value.find(d => d.DNO === dno)
      if (dish) {
        newPrice.value = dish.DPRICE
      }
    }

    // 更新价格
    const updatePrice = async (dno: string) => {
      if (newPrice.value !== null) {
        await axios.put('/api/dish/update_price', {
          DNO: dno,
          DPRICE: newPrice.value
        })
        editingDish.value = null // 结束编辑
        await load() // 刷新菜品列表
      }
    }

    // 取消编辑
    const cancelEdit = () => {
      editingDish.value = null
    }

    onMounted(load)

    return { 
      dishes, 
      newDish, 
      addDish, 
      removeDish, 
      editPrice, 
      updatePrice, 
      cancelEdit, 
      editingDish, 
      newPrice 
    }
  }
})
</script>

<style scoped>
/* 按钮样式 */
button {
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

/* 输入框和按钮的布局 */
input[type="text"], input[type="number"] {
  font-size: 1rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  transition: all 0.3s ease;
}

input[type="text"]:focus, input[type="number"]:focus {
  border-color: #1d4ed8;
  outline: none;
}

/* 菜品列表样式 */
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

li img {
  border-radius: 8px;
}

/* 输入框的样式 */
input[type="text"], input[type="number"], button {
  border-radius: 0.375rem;
  padding: 0.5rem;
}
</style>
