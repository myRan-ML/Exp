<template>
  <div class="bg-white p-6 rounded shadow mt-8">
    <h2 class="text-xl font-semibold mb-4">📜 历史订单</h2>
    <div v-if="orders.length">
      <div
        v-for="order in orders"
        :key="order.oid"
        class="border p-4 rounded mb-4 bg-gray-50 shadow-sm"
      >
        <p class="text-gray-700 mb-2">订单号：{{ order.oid }}</p>
        <p class="text-gray-500 text-sm mb-1">下单时间：{{ order.order_time }}</p>
        <p class="text-gray-500 text-sm mb-2">总金额：¥{{ order.total }}</p>
        <ul class="ml-4 text-sm text-gray-600">
          <li v-for="item in order.items" :key="item.DNO">
            {{ item.DNAME }} x {{ item.QUANTITY }} @ ¥{{ item.PRICE_AT_ORDER }}
          </li>
        </ul>
      </div>
    </div>
    <div v-else class="text-gray-500">暂无订单。</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'OrderHistory',
  setup() {
    const orders = ref<any[]>([])

    const fetchOrders = async () => {
      try {
        const uid = localStorage.getItem('uid')
        if (!uid) return

        const res = await axios.get(`/api/order/user/${uid}`)
        orders.value = res.data
      } catch (e) {
        console.error('获取订单失败', e)
      }
    }

    onMounted(fetchOrders)
    return { orders }
  }
})
</script>
