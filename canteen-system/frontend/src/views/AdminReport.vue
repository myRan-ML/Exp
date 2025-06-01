<template>
  <div class="p-6">
    <h2 class="text-2xl font-semibold mb-4">📈 销售报表</h2>
    <div class="mb-4 flex gap-4">
      <input v-model="start" type="date" class="border p-2 rounded" />
      <input v-model="end" type="date" class="border p-2 rounded" />
      <button @click="generate" class="bg-blue-500 text-white px-4 py-2 rounded">生成报表</button>
    </div>
    <div v-if="report">
      <p class="mb-2">总销售额：¥{{ report.total_sales }}</p>
      <ul>
        <li v-for="order in report.orders" :key="order.OID" class="mb-1 text-sm text-gray-700">
          订单号：{{ order.OID }}，金额：¥{{ order.TOTAL_AMOUNT }}，时间：{{ order.ORDER_TIME }}
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

    const generate = async () => {
      const res = await axios.post('/api/order/report', {
        start: start.value,
        end: end.value
      })
      report.value = res.data
    }

    return { start, end, report, generate }
  }
})
</script>
