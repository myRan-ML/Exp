import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './index.css'  // Tailwind 引入

createApp(App)
  .use(router)
  .mount('#app')