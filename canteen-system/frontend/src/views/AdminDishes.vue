<template>
  <div class="p-6">
    <h2 class="text-2xl font-semibold mb-4">🍲 菜品管理</h2>
    <form @submit.prevent="addDish" class="mb-6 flex gap-4">
      <input v-model="newDish.DNO" placeholder="编号" class="border p-2 rounded" />
      <input v-model="newDish.DNAME" placeholder="名称" class="border p-2 rounded" />
      <input v-model="newDish.DPRICE" placeholder="价格" type="number" class="border p-2 rounded" />
      <button class="bg-green-500 text-white px-4 py-2 rounded">添加</button>
    </form>
    <ul class="space-y-2">
      <li v-for="dish in dishes" :key="dish.DNO" class="p-4 border rounded bg-gray-50 flex justify-between">
        {{ dish.DNAME }} - ¥{{ dish.DPRICE }}
        <button @click="removeDish(dish.DNO)" class="text-red-500 hover:underline">删除</button>
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
}

export default defineComponent({
  setup() {
    const dishes = ref<Dish[]>([])
    const newDish = ref<Dish>({ DNO: '', DNAME: '', DPRICE: 0 })

    const load = async () => {
      const res = await axios.get('/api/dish/all')
      dishes.value = res.data
    }

    const addDish = async () => {
      await axios.post('/api/dish/add', newDish.value)
      newDish.value = { DNO: '', DNAME: '', DPRICE: 0 }
      await load()
    }

    const removeDish = async (dno: string) => {
      await axios.delete(`/api/dish/delete/${dno}`)
      await load()
    }

    onMounted(load)
    return { dishes, newDish, addDish, removeDish }
  }
})
</script>
