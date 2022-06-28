<template>
  <div id="app">
    <Map/>
    <sidebar id="sidebar"></sidebar>
    <routeshow></routeshow>

  </div>

</template>

<script>
import sidebar from "./components/sidebar";

import routeshow from "./components/routeshow";



export default {
  name: "App",
  components: {
    routeshow,
    sidebar
  }
};
</script>
