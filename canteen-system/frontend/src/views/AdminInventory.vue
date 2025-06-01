<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-4">📦 库存管理</h2>
    <div v-if="inventory.length">
      <table class="table-auto w-full border text-center">
        <thead>
          <tr>
            <th class="border px-4 py-2">菜品编号</th>
            <th class="border px-4 py-2">名称</th>
            <th class="border px-4 py-2">库存</th>
            <th class="border px-4 py-2">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in inventory" :key="item.DNO">
            <td class="border px-4 py-2">{{ item.DNO }}</td>
            <td class="border px-4 py-2">{{ item.DNAME }}</td>
            <td class="border px-4 py-2">
              <input
                type="number"
                v-model.number="item.STOCK"
                class="border rounded w-20 text-center"
                min="0"
              />
            </td>
            <td class="border px-4 py-2">
              <button
                @click="updateStock(item)"
                class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
              >
                保存
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="text-gray-500">暂无库存数据</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'
import axios from 'axios'

interface InventoryItem {
  DNO: string
  DNAME: string
  STOCK: number
}

export default defineComponent({
  name: 'AdminInventory',
  setup() {
    const inventory = ref<InventoryItem[]>([])

    const fetchInventory = async () => {
      try {
        const res = await axios.get('/api/inventory/all')
        inventory.value = res.data
      } catch (e) {
        console.error('获取库存失败', e)
      }
    }

    const updateStock = async (item: InventoryItem) => {
      try {
        const res = await axios.post('/api/inventory/update', {
          dno: item.DNO,
          stock: item.STOCK
        })
        alert(`库存更新成功: ${res.data.message}`)
      } catch (e) {
        console.error('更新库存失败', e)
        alert('库存更新失败')
      }
    }

    onMounted(fetchInventory)
    return { inventory, updateStock }
  }
})
</script>
