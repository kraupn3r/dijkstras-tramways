import VueRouter from "vue-router";
import home from "./pages/home.vue";
// configure router
const router = new Router({
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

export default router;
