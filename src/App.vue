<template>
  <div id="app">
    <Map/>
    <sidebar id="sidebar"></sidebar>
    <routeshow></routeshow>

  </div>

</template>

<script>
import sidebar from "./components/sidebar.js";

import routeshow from "./components/routeshow.js";



export default {
  name: "App",
  components: {
    routeshow,
    sidebar
  }
};
</script>
