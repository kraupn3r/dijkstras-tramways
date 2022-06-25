import Vue from "vue";
import VueRouter from "vue-router";
import App from "./App.vue";
import store from "./store"
import router from "./router";
import { Icon } from "leaflet";

import VueCookies from 'vue-cookies';
import "leaflet/dist/leaflet.css";
// delete Icon.Default.prototype._getIconUrl;
// Icon.Default.mergeOptions({
//   iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
//   iconUrl: require("leaflet/dist/images/marker-icon.png"),
//   shadowUrl: require("leaflet/dist/images/marker-shadow.png")
// });
//

// Vue.use(VueRouter);
Vue.use(VueCookies);
new Vue({
  // router,
  store,
  render: h => h(App)
}).$mount("#app");

// export {app, store}
