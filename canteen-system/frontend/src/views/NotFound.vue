<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-6xl font-bold">404</h1>
      <p class="text-xl mt-4">页面未找到</p>
      <router-link to="/" class="mt-6 inline-block text-blue-500 hover:underline">返回首页</router-link>
    </div>
  </div>
</template>

<script lang="ts">
export default { name: 'NotFound' }
</script>