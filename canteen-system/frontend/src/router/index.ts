import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import CustomerDashboard from '../views/CustomerDashboard.vue'
import NotFound from '../views/NotFound.vue'
import OrderHistory from '../components/OrderHistory.vue'


const routes: Array<RouteRecordRaw> = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin', component: AdminDashboard },
  { path: '/customer', component: CustomerDashboard },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  { path: '/order-history', component: OrderHistory },
  {
    path: '/admin',
    component: () => import('../views/AdminDashboard.vue')
  },
  {
    path: '/admin/employees',
    component: () => import('../views/AdminEmployees.vue')
  },
  {
    path: '/admin/dishes',
    component: () => import('../views/AdminDishes.vue')
  },
  {
    path: '/admin/inventory',
    component: () => import('../views/AdminInventory.vue')
  },
  {
    path: '/admin/report',
    component: () => import('../views/AdminReport.vue')
  },
  {
  path: '/admin/window',
  name: 'AdminWindow',
  component: () => import('../views/DscManage.vue')
}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router