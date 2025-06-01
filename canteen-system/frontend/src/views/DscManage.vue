<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">🍱 菜品窗口管理</h2>

    <!-- 添加窗口信息表单 -->
    <div class="mb-6 space-y-3">
      <h3 class="text-xl font-semibold">添加窗口信息</h3>
      <div>
        <label>菜品：</label>
        <select v-model="form.DNO" class="border p-1 rounded w-64">
          <option disabled value="">请选择菜品</option>
          <option v-for="dish in dishes" :key="dish.DNO" :value="dish.DNO">
            {{ dish.DNO }} - {{ dish.DNAME }}
          </option>
        </select>
      </div>
      <div>
        <label>窗口号：</label>
        <input v-model="form.DWIN" type="text" class="border p-1 rounded w-64" />
      </div>
      <div>
        <label>时间段：</label>
        <select v-model="form.DTIME" class="border p-1 rounded w-64">
          <option value="mor">早</option>
          <option value="aft">中</option>
          <option value="eve">晚</option>
        </select>
      </div>
      <button @click="addDsc" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        添加窗口信息
      </button>
    </div>

    <!-- 查询窗口对应菜品 -->
    <div class="mb-6">
      <h3 class="text-xl font-semibold mb-2">查询窗口菜品</h3>
      <div class="flex gap-2 mb-2">
        <input v-model="queryWin" placeholder="输入窗口号" class="border p-1 rounded w-64" />
        <button @click="fetchByWindow" class="bg-green-500 text-white px-4 py-1 rounded hover:bg-green-600">
          查询
        </button>
      </div>
    </div>

    <!-- 结果显示 -->
    <div v-if="results.length">
      <table class="table-auto w-full border">
        <thead>
          <tr>
            <th class="border px-4 py-2">编号</th>
            <th class="border px-4 py-2">名称</th>
            <th class="border px-4 py-2">价格</th>
            <th class="border px-4 py-2">窗口</th>
            <th class="border px-4 py-2">时间段</th>
            <th class="border px-4 py-2">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in results" :key="item.DNO + item.DWIN + item.DTIME">
            <td class="border px-4 py-2">{{ item.DNO }}</td>
            <td class="border px-4 py-2">{{ item.DNAME }}</td>
            <td class="border px-4 py-2">{{ item.DPRICE }}</td>
            <td class="border px-4 py-2">{{ item.DWIN }}</td>
            <td class="border px-4 py-2">{{ timeLabel(item.DTIME) }}</td>
            <td class="border px-4 py-2">
              <button @click="deleteDsc(item)" class="text-red-500 hover:underline">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="text-gray-500">暂无记录</div>
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

    const fetchDishes = async () => {
      try {
        const res = await axios.get('/api/dish/all')
        dishes.value = res.data
      } catch (err) {
        console.error('获取菜品失败', err)
      }
    }

    const fetchByWindow = async () => {
      if (!queryWin.value) {
        alert('请输入窗口号')
        return
      }
      const res = await axios.get('/api/dsc/by_window', {
        params: { win: queryWin.value }
      })
      results.value = res.data
    }

    const addDsc = async () => {
      if (!form.value.DNO || !form.value.DWIN || !form.value.DTIME) {
        alert('请填写完整信息')
        return
      }
      await axios.post('/api/dsc/add', form.value)
      alert('添加成功')
      fetchByWindow()
    }

    const deleteDsc = async (item: any) => {
      await axios.delete('/api/dsc/delete', {
        params: {
          dno: item.DNO,
          dwin: item.DWIN,
          dtime: item.DTIME
        }
      })
      alert('删除成功')
      fetchByWindow()
    }

    const timeLabel = (code: string) => {
      return code === 'mor' ? '早' : code === 'aft' ? '中' : '晚'
    }

    onMounted(fetchDishes)

    return {
      form, queryWin, results, dishes,
      fetchDishes, fetchByWindow, addDsc, deleteDsc,
      timeLabel
    }
  }
})
</script>
