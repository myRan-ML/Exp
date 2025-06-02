<template>
  <div class="p-6 bg-white rounded-lg shadow-md">
    <!-- 标题 -->
    <h2 class="text-3xl font-semibold mb-6 text-gray-800">📈 销售报表</h2>

    <!-- 日期选择器和生成按钮 -->
    <div class="mb-6 flex gap-6 justify-start items-center">
      <input
        v-model="start"
        type="date"
        class="border p-2 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
      />
      <input
        v-model="end"
        type="date"
        class="border p-2 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
      />
      <button
        @click="generate"
        class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-all"
      >
        生成报表
      </button>
    </div>

    <!-- 显示报表数据 -->
    <div v-if="report" class="space-y-4">
      <p class="text-xl font-medium text-gray-800">总销售额：<span class="text-blue-600">¥{{ report.total_sales }}</span></p>
      
      <!-- 订单列表 -->
      <ul>
        <li
          v-for="order in report.orders"
          :key="order.OID"
          class="bg-gray-50 border border-gray-200 rounded-lg mb-4 p-4 shadow-sm hover:bg-gray-100 transition-all"
        >
          <div class="flex justify-between items-center">
            <div>
              <p class="text-lg font-semibold text-gray-800">订单号：{{ order.OID }}</p>
              <p class="text-sm text-gray-600">时间：{{ order.ORDER_TIME }}</p>
            </div>
            <p class="text-lg text-blue-600 font-medium">¥{{ order.TOTAL_AMOUNT }}</p>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from 'axios'

export default defineComponent({
  setup() {
    const start = ref('')
    const end = ref('')
    const report = ref<any>(null)

    // 生成报表
    const generate = async () => {
      try {
        const res = await axios.post('/api/order/report', {
          start: start.value,
          end: end.value
        })
        report.value = res.data
      } catch (error) {
        console.error('生成报表失败', error)
      }
    }

    return { start, end, report, generate }
  }
})
</script>

<style scoped>
/* 基本布局优化 */
p {
  line-height: 1.5;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  transition: transform 0.3s ease, background-color 0.2s ease;
}

li:hover {
  transform: translateY(-5px);
  background-color: #f9fafb;
}

/* 按钮、输入框样式 */
button {
  transition: all 0.3s ease;
}

input[type="date"] {
  font-size: 1rem;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
}

input[type="date"]:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

/* 优化提示框 */
.bg-gray-50 {
  background-color: #f9fafb;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .flex {
    flex-direction: column;
    gap: 4px;
  }
  .p-6 {
    padding: 2rem;
  }
}
</style>
