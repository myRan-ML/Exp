<template>
  <div>
    <h2 class="text-2xl font-semibold mb-4">库存管理</h2>
    <table class="min-w-full bg-white">
      <thead>
        <tr>
          <th class="py-2 px-4 border">菜品编号</th>
          <th class="py-2 px-4 border">菜名</th>
          <th class="py-2 px-4 border">库存</th>
          <th class="py-2 px-4 border">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in inventory" :key="item.DNO">
          <td class="py-2 px-4 border">{{ item.DNO }}</td>
          <td class="py-2 px-4 border">{{ item.DNAME }}</td>
          <td class="py-2 px-4 border">{{ item.STOCK }}</td>
          <td class="py-2 px-4 border">
            <input type="number" v-model.number="newStocks[item.DNO]" class="w-16 p-1 border rounded mr-2" />
            <button @click="updateStock(item.DNO)" class="bg-blue-500 text-white py-1 px-3 rounded hover:bg-blue-600 transition">更新</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'

interface InventoryItem { DNO: string; DNAME: string; STOCK: number }

export default defineComponent({
  name: 'Inventory',
  setup() {
    const inventory = ref<InventoryItem[]>([])
    const newStocks = ref<Record<string, number>>({})

    const fetchInventory = async () => {
      const res = await axios.get('/api/inventory')
      inventory.value = res.data
      inventory.value.forEach(i => {
        newStocks.value[i.DNO] = i.STOCK
      })
    }

    const updateStock = async (dno: string) => {
      try {
        await axios.post('/api/update_stock', { DNO: dno, new_stock: newStocks.value[dno] })
        alert('库存更新成功')
        fetchInventory()
      } catch {
        alert('更新失败')
      }
    }

    onMounted(fetchInventory)
    return { inventory, newStocks, updateStock }
  }
})
</script>