<template>
  <div id="app">
    <Map/>
    <sidebar id="sidebar"></sidebar>
    <routeshow></routeshow>

  </div>

</template>

<script>
import Map from "./components/map";
import Sidebar from "./components/sidebar";
import Routeshow from "./components/routeshow";



export default {
  name: "App",
  components: {
    Map,
    Routeshow,
    Sidebar
  }
};
</script>
