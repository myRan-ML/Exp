<template>
  <div class="p-6 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-4 text-gray-800">📦 库存管理</h2>

    <!-- 库存列表 -->
    <div v-if="inventory.length">
      <table class="table-auto w-full border border-gray-300 text-center mb-6">
        <thead>
          <tr class="bg-gray-100 text-sm text-gray-600">
            <th class="border px-4 py-2">菜品编号</th>
            <th class="border px-4 py-2">名称</th>
            <th class="border px-4 py-2">库存</th>
            <th class="border px-4 py-2">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in inventory" :key="item.DNO" class="bg-white hover:bg-gray-50 transition-colors">
            <td class="border px-4 py-2 text-sm">{{ item.DNO }}</td>
            <td class="border px-4 py-2 text-sm">{{ item.DNAME }}</td>
            <td class="border px-4 py-2">
              <input
                type="number"
                v-model.number="item.STOCK"
                class="border rounded-lg w-24 p-2 text-center"
                min="0"
                :class="{'border-red-500': item.STOCK < 0}"
              />
            </td>
            <td class="border px-4 py-2">
              <button
                @click="updateStock(item)"
                class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 focus:outline-none transition-all"
              >
                保存
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 无库存数据时显示 -->
    <div v-else class="text-gray-500 text-lg">
      暂无库存数据
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
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

    // 获取库存数据
    const fetchInventory = async () => {
      try {
        const res = await axios.get('/api/inventory/all')
        inventory.value = res.data
      } catch (e) {
        console.error('获取库存失败', e)
      }
    }

    // 更新库存
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

    // 初始加载库存
    onMounted(fetchInventory)
    
    return { inventory, updateStock }
  }
})
</script>

<style scoped>
/* 响应式设计 */
@media (max-width: 768px) {
  .table-auto {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
}

/* 统一按钮样式 */
button {
  transition: all 0.3s ease;
}

button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

input[type="number"] {
  font-size: 1rem;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 0.375rem;
}

input[type="number"]:focus {
  border-color: #1d4ed8;
  outline: none;
}
</style>
