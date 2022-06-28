import Vue from 'vue'
import App from '@/App.vue'

import store from '@/store'
// import router from '@/router'
import "leaflet/dist/leaflet.css";
Vue.config.productionTip = false
import { Icon } from "leaflet";
// Vue.use(VueRouter)

const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')
