<template>
  <div class="p-6 bg-white rounded-lg shadow-md">
    <!-- 标题 -->
    <div class="flex justify-between items-center mb-6">
      <!-- 南航校徽 -->
      <img src="../../images/nuaa_logo.jpg" alt="南航校徽" class="h-12" />
      <h2 class="text-3xl font-bold text-gray-800">🍱 菜品窗口管理</h2>
      <!-- 南航食堂标志 -->
      <img src="../../images/canteen_logo.jpg" alt="食堂标志" class="h-12" />
    </div>

    <!-- 添加窗口信息表单 -->
    <div class="mb-6 space-y-4">
      <h3 class="text-xl font-semibold text-gray-700">添加窗口信息</h3>
      
      <!-- 表单 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label for="dish" class="block text-gray-600">菜品：</label>
          <select id="dish" v-model="form.DNO" class="w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 transition-all">
            <option disabled value="">请选择菜品</option>
            <option v-for="dish in dishes" :key="dish.DNO" :value="dish.DNO">
              {{ dish.DNO }} - {{ dish.DNAME }}
            </option>
          </select>
        </div>
        
        <div>
          <label for="window" class="block text-gray-600">窗口号：</label>
          <input id="window" v-model="form.DWIN" type="text" class="w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 transition-all" />
        </div>

        <div>
          <label for="time" class="block text-gray-600">时间段：</label>
          <select id="time" v-model="form.DTIME" class="w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 transition-all">
            <option value="mor">早</option>
            <option value="aft">中</option>
            <option value="eve">晚</option>
          </select>
        </div>
      </div>

      <!-- 添加按钮 -->
      <button @click="addDsc" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 transition-all">
        添加窗口信息
      </button>
    </div>

    <!-- 查询窗口对应菜品 -->
    <div class="mb-6">
      <h3 class="text-xl font-semibold text-gray-700 mb-2">查询窗口菜品</h3>
      <div class="flex gap-4 mb-4">
        <input v-model="queryWin" placeholder="输入窗口号" class="w-full p-3 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 transition-all" />
        <button @click="fetchByWindow" class="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 focus:ring-2 focus:ring-green-500 transition-all">
          查询
        </button>
      </div>
    </div>

    <!-- 结果显示 -->
    <div v-if="results.length">
      <table class="min-w-full table-auto bg-white border rounded-lg shadow-md">
        <thead class="bg-blue-600 text-white">
          <tr>
            <th class="px-6 py-4 text-left">编号</th>
            <th class="px-6 py-4 text-left">名称</th>
            <th class="px-6 py-4 text-left">价格</th>
            <th class="px-6 py-4 text-left">窗口</th>
            <th class="px-6 py-4 text-left">时间段</th>
            <th class="px-6 py-4 text-center">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in results" :key="item.DNO + item.DWIN + item.DTIME" class="border-b hover:bg-gray-50 transition-all">
            <td class="px-6 py-4">{{ item.DNO }}</td>
            <td class="px-6 py-4">{{ item.DNAME }}</td>
            <td class="px-6 py-4">¥{{ item.DPRICE }}</td>
            <td class="px-6 py-4">{{ item.DWIN }}</td>
            <td class="px-6 py-4">{{ timeLabel(item.DTIME) }}</td>
            <td class="px-6 py-4 text-center">
              <button @click="deleteDsc(item)" class="text-red-500 hover:underline">
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="text-gray-500">暂无记录</div>

    <!-- 提示框 -->
    <div v-if="message" class="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50">
      {{ message }}
    </div>

    <div v-if="errorMessage" class="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'DscManage',
  setup() {
    const form = ref({ DNO: '', DWIN: '', DTIME: 'mor' })
    const queryWin = ref('')
    const results = ref<any[]>([])
    const dishes = ref<any[]>([])
    const message = ref('')
    const errorMessage = ref('')

    // 获取菜品列表
    const fetchDishes = async () => {
      try {
        const res = await axios.get('/api/dish/all')
        dishes.value = res.data
      } catch (err) {
        console.error('获取菜品失败', err)
      }
    }

    // 根据窗口号查询菜品
    const fetchByWindow = async () => {
      if (!form.value.DWIN) {
        alert('请输入窗口号')
        return
      }
      const res = await axios.get('/api/window/by_window', {
        params: { win: form.value.DWIN }
      })
      results.value = res.data
    }

    // 添加窗口信息
    const addDsc = async () => {
      if (!form.value.DNO || !form.value.DWIN || !form.value.DTIME) {
        alert('请填写完整信息')
        return
      }
      try {
        await axios.post('/api/window/add', form.value)
        message.value = '添加窗口信息成功!'
        fetchByWindow()
      } catch (e) {
        errorMessage.value = '添加窗口信息失败!'
      }
    }

    // 删除窗口信息
    const deleteDsc = async (item: any) => {
      try {
        await axios.delete('/api/window/delete', {
          params: {
            dno: item.DNO,
            dwin: item.DWIN,
            dtime: item.DTIME
          }
        })
        message.value = '删除窗口信息成功!'
        fetchByWindow()
      } catch (e) {
        errorMessage.value = '删除窗口信息失败!'
      }
    }

    // 显示时间段
    const timeLabel = (code: string) => {
      return code === 'mor' ? '早' : code === 'aft' ? '中' : '晚'
    }

    onMounted(fetchDishes)

    return {
      form, queryWin, results, dishes,
      fetchDishes, fetchByWindow, addDsc, deleteDsc,
      timeLabel, message, errorMessage
    }
  }
})
</script>

<style scoped>
/* 按钮、输入框和表格的样式美化 */
button {
  transition: all 0.3s ease;
}

input[type="text"], input[type="date"], select {
  font-size: 1rem;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: #f9fafb;
  transition: all 0.3s ease;
}

input[type="text"]:focus, select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

/* 表格样式 */
table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #3b82f6;
}

th, td {
  padding: 1rem;
  border: 1px solid #ddd;
}

th {
  text-align: left;
}

tbody tr:hover {
  background-color: #f1f5f9;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }

  .flex {
    flex-direction: column;
  }
}
</style>
