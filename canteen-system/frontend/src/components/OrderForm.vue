<template>
  <div class="bg-white p-6 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">🛒 我的购物车</h2>

    <div v-if="cartItems.length">
      <ul class="mb-4">
        <li
          v-for="item in cartItems"
          :key="item.DNO"
          class="flex justify-between items-center border-b py-2"
        >
          <span>{{ item.DNAME }} x {{ item.quantity }}</span>
          <button
            @click="remove(item.DNO)"
            class="text-red-500 hover:underline"
          >
            移除
          </button>
        </li>
      </ul>
      <button
        @click="submitOrder"
        :disabled="submitting"
        class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
      >
        {{ submitting ? "正在提交..." : "提交订单" }}
      </button>
    </div>
    <div v-else class="text-gray-500">购物车为空。</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, watch } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'OrderForm',
  props: {
    cartItems: {
      type: Array as PropType<any[]>,
      required: true
    },
    removeFromCart: {
      type: Function,
      required: true
    }
  },
  emits: ['order-success', 'order-failed'],
  setup(props, { emit }) {
    const submitting = ref(false)

    const remove = (dno: string) => {
      props.removeFromCart(dno)
    }

    const submitOrder = async () => {
      if (!props.cartItems.length) return
      const uid = localStorage.getItem('uid')
      if (!uid) {
        emit('order-failed', '请重新登录')
        return
      }

      submitting.value = true

      try {
        const res = await axios.post('/api/order/place', {
          uid: parseInt(uid),
          cart: props.cartItems.map((item) => ({
            dno: item.DNO,
            quantity: item.quantity
          }))
        })

        emit('order-success', res.data.message || '订单已成功提交')
      } catch (err: any) {
        const msg = err.response?.data?.error || '提交订单失败'
        emit('order-failed', msg)
      } finally {
        submitting.value = false
      }
    }

    return { remove, submitOrder, submitting }
  }
})
</script>
