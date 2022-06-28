import Vue from 'vue'
import Router from 'vue-router'
import home from "@/pages/home.vue";
Vue.use(Router)

export default new Router({
  routes: [
    mode: 'History',
    base: '/app',
    routes: [
     {
       path: '/',
       name: 'map',
       component: Map
     }

  ]
})
