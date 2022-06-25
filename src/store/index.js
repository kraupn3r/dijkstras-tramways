import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state:  {
    walkvals: [],
    startTramStop: "",
    endTramStop: "",
    startTramStopLatLng: [],
    stopTramStopLatLng: [],
    routeChapterArray: null,
    startPointLatLng: ['', ''],
    endPointLatLng: ['', ''],
    pickedLatLng: [],
    mouselatlng: []
  },
  mutations: {},
  actions: {},
  modules: {},
});
