<template>
  <div id="app">
    <Map/>
    <sidebar id="sidebar"></sidebar>
    <routeshow></routeshow>

  </div>

</template>

<script>
import Map from "./components/map";
import Sidebar from "./components/Sidebar";
import Routeshow from "./components/Routeshow";



export default {
  name: "App",
  components: {
    Map,
    Routeshow,
    Sidebar
  }
};
</script>

<style></style>
