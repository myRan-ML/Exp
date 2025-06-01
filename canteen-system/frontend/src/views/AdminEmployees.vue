<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <h2 class="text-3xl font-semibold mb-6 text-center text-indigo-600">👷 员工管理</h2>

    <!-- 添加员工表单 -->
    <form @submit.prevent="addEmployee" class="mb-8 flex flex-col sm:flex-row gap-6 bg-white shadow-lg rounded-xl p-6">
      <input v-model="newEid" type="number" placeholder="员工编号" class="border border-gray-300 p-3 rounded-lg w-full sm:w-1/4 focus:outline-none focus:ring-2 focus:ring-indigo-400" />
      <input v-model="newName" placeholder="姓名" class="border border-gray-300 p-3 rounded-lg w-full sm:w-1/4 focus:outline-none focus:ring-2 focus:ring-indigo-400" />
      <input v-model="newRole" placeholder="岗位" class="border border-gray-300 p-3 rounded-lg w-full sm:w-1/4 focus:outline-none focus:ring-2 focus:ring-indigo-400" />
      <select v-model="newSex" class="border border-gray-300 p-3 rounded-lg w-full sm:w-1/4 focus:outline-none focus:ring-2 focus:ring-indigo-400">
        <option value="male">男</option>
        <option value="female">女</option>
      </select>
      <input v-model="newSalary" type="number" placeholder="薪水" class="border border-gray-300 p-3 rounded-lg w-full sm:w-1/4 focus:outline-none focus:ring-2 focus:ring-indigo-400" />
      <button class="bg-gradient-to-r from-green-400 to-teal-500 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 hover:scale-105 hover:from-green-500 hover:to-teal-600">
        添加
      </button>
    </form>

    <!-- 员工列表 -->
    <ul class="space-y-4">
      <li v-for="emp in employees" :key="emp.ENO" class="p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-300">
        <div class="flex justify-between items-center">
          <div>
            <p class="text-lg font-medium text-indigo-600">{{ emp.ENAME }}</p>
            <p class="text-sm text-gray-500">原岗位: {{ emp.EJOB }} | 原薪水: ¥{{ emp.ESAL }}</p>
          </div>
          <button @click="deleteEmployee(emp.ENO)" class="text-red-500 hover:text-red-700 transition-all duration-200">删除</button>
        </div>
        
        <div class="mt-4 flex gap-4">
          <div class="w-full">
            <input v-model="newSalary[emp.ENO]" placeholder="新薪水" class="border border-gray-300 p-3 rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-indigo-400" />
            <button @click="updateSalary(emp.ENO)" class="mt-2 bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg w-full transition-all duration-300 hover:bg-blue-600">
              更新薪水
            </button>
          </div>
          <div class="w-full">
            <input v-model="newJob[emp.ENO]" placeholder="新岗位" class="border border-gray-300 p-3 rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-indigo-400" />
            <button @click="updateJob(emp.ENO)" class="mt-2 bg-orange-500 text-white font-semibold py-2 px-4 rounded-lg w-full transition-all duration-300 hover:bg-orange-600">
              更新岗位
            </button>
          </div>
        </div>
      </li>
    </ul>

    <!-- 提示区域 -->
    <div v-if="message" class="mt-8 p-4 bg-green-200 text-green-800 rounded-lg shadow-md">
      {{ message }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'

interface Employee {
  ENO: number
  ENAME: string
  ESEX: string
  EJOB: string
  ESAL: number
}

export default defineComponent({
  setup() {
    const employees = ref<Employee[]>([])
    const newEid = ref<number | null>(null)
    const newName = ref('')
    const newRole = ref('')
    const newSex = ref('male')
    const newSalary = ref<Record<number, number>>({})
    const newJob = ref<Record<number, string>>({})
    const message = ref('')

    // 加载员工数据
    const load = async () => {
      const res = await axios.get('/api/employee/all')
      employees.value = res.data
      employees.value.forEach(emp => {
        newSalary.value[emp.ENO] = emp.ESAL
        newJob.value[emp.ENO] = emp.EJOB
      })
    }

    // 添加新员工
    const addEmployee = async () => {
      if (!newEid.value || newEid.value <= 0) {
        alert('请输入有效的员工编号 (ENO)')
        return
      }
      if (newSalary.value == null) {
        alert('请输入有效的薪水')
        return
      }

      const employeeData = {
        ENO: newEid.value,
        ENAME: newName.value,
        ESEX: newSex.value,
        EJOB: newRole.value,
        ESAL: newSalary.value
      }

      try {
        const res = await axios.post('/api/employee/add', employeeData)
        alert(res.data.message)
        newEid.value = null
        newName.value = ''
        newRole.value = ''
        newSex.value = 'male'
        newSalary.value = {}
        await load()
      } catch (error) {
        console.error('添加员工失败:', error)
        alert('添加失败，请检查后端接口或参数')
      }
    }

    // 删除员工
    const deleteEmployee = async (eno: number) => {
      await axios.delete(`/api/employee/delete?eno=${eno}`)
      await load()
    }

    // 更新薪水
    const updateSalary = async (eno: number) => {
      const salary = newSalary.value[eno]
      if (salary <= 0) {
        alert('请输入有效的薪水')
        return
      }

      try {
        await axios.post('/api/employee/update_salary', {
          ENO: eno,
          ESAL: salary
        })
        await load()
        message.value = "员工薪水更新成功!"
      } catch (error) {
        console.error('薪水更新失败:', error)
        message.value = "薪水更新失败，请重试!"
      }
    }

    // 更新岗位
    const updateJob = async (eno: number) => {
      const job = newJob.value[eno]
      if (job) {
        try {
          await axios.post('/api/employee/update_job', {
            ENO: eno,
            EJOB: job
          })
          await load()
          message.value = "员工岗位更新成功!"
        } catch (error) {
          console.error('岗位更新失败:', error)
          message.value = "岗位更新失败，请重试!"
        }
      }
    }

    // 加载页面时获取员工数据
    onMounted(load)

    return {
      employees,
      newEid,
      newName,
      newRole,
      newSex,
      newSalary,
      newJob,
      message,
      addEmployee,
      deleteEmployee,
      updateSalary,
      updateJob
    }
  }
})
</script>

<style scoped>
/* 轻微阴影效果 */
.shadow-lg {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* 渐变按钮效果 */
.bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops));
}

.transition-all {
  transition: all 0.3s ease-in-out;
}

.hover\:scale-105:hover {
  transform: scale(1.05);
}
</style>
