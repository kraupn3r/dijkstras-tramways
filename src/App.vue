<template>
  <div id="app">
    <Map/>
    <sidebar id="sidebar"></sidebar>
    <routeshow></routeshow>

  </div>

</template>

<script>
import Sidebar from "@/components/sidebar";
import map from "@/components/map";
import Routeshow from "@/components/routeshow";



export default {
  name: "App",
  components: {
    routeshow,
    sidebar
  }
};
</script>
