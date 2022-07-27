<template>
   <div id="app">
    <Map/>
    <sidebar id="sidebar"></sidebar>
    <routeshow></routeshow>

  </div>

</template>

<script>
import Sidebar from "./components/Sidebar";
import Map from "./components/map"; 
import Routeshow from "./components/Routeshow";
export default {
  name: 'App',
  components: {
     Routeshow,
    Map,
    Sidebar,
  }
}
</script>

<style>
@import './assets/css/style.css'; 
</style>
