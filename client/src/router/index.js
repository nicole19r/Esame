import { createRouter, createWebHistory } from 'vue-router'
import analysis from '../components/Analysis.vue'

//Definizione del router
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'analysis',
      component: analysis
    },
  ]
})

export default router
