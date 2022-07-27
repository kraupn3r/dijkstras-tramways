<template>
<div id="sidebarContain" >
<div class="stopParagraph">
<div class="searchContainer">
<div class="separator">  <div class="iconContain"><div class="starticonA"></div></div></div>
    <input readonly onfocus="this.removeAttribute('readonly');" autocomplete="off" id="sidebar-search" v-on:click="first_col_watch(searchterm)" class="stopSearch" type="text" v-model="searchterm" ><div class="separator"> <div v-on:click="clear_Ainput()" id="Apcross"  class="iconContain"><div  id="startRightIcon"></div></div></div></div>
<ul id="first_column" class="butColumn">
        <li class="stopli" v-for="stop in searchset" :key="stop.id" v-on:click="pickStartingPoint(stop)">
      <div class="iconWrapper">  <div class="tramIcon"></div></div> <span> {(stop.name)}</span>
        </li>
    </ul></div>

    <div class="stopParagraph">
    <div class="searchContainer">
    <div class="separator">   <div class="iconContain"><div class="starticonb"></div></div></div>
        <input readonly onfocus="this.removeAttribute('readonly');" autocomplete="off" id="sidebar-search_two" v-on:click="second_col_watch(searchterm_two)" class="stopSearch" type="text" v-model="searchterm_two" ><div class="separator"> <div v-on:click="clear_Binput()" id="Bpcross" class="iconContain"><div id="startRightIcon"></div></div></div></div>
        <ul id="second_column" class="butColumn">
            <li class="stopli" v-for="stop in searchset_two" :key="stop.id" v-on:click="pickEndingPoint(stop)">
        <div class="iconWrapper">  <div class="tramIcon"></div></div> <span> {(stop.name)}</span>
            </li>
        </ul></div>
<div class="inputBar">
    <input type="time" id="stime" :value="(new Date()).toTimeString().substr(0,5)">
  <button id="find-route" v-on:click="fetchAPIData"><div class="routeicon"></div></button>

</div>
</div>
</template>

<script>
import { EventBus } from "../main"
export default {
  name: "Sidebar", // eslint-disable-line vue/multi-word-component-names
  delimiters: ['{(', ')}'],
    data() {
      return {
        searchterm: '',
        searchterm_two: '',
        timeout: null,
        sharedState: this.$store.state,
        searchset: [],
        searchset_two: []
      }
    },
    mounted() {
      const self = this
      EventBus.$on('fetchh',() =>{

        self.fetchAPIData()

      });
      EventBus.$on('pickStartPointLatLng', () => {
        this.searchterm = "A point on map"
        this.$store.state.startTramStop = ""
        this.$store.state.startPointLatLng = this.$store.state.pickedLatLng
      });
      EventBus.$on('pickEndPointLatLng', () => {
        this.searchterm_two = "A point on map"
        this.$store.state.endTramStop = ""
        this.$store.state.endPointLatLng = this.$store.state.pickedLatLng

      });
    },
    watch: {
      searchterm(){
        this.first_col_watch(this.searchterm)
      },
      searchterm_two(){
        this.second_col_watch(this.searchterm_two)
      }
    },
    methods: {
      clear_Binput() {

        document.getElementById("sidebar-search_two").value = "";
        this.searchterm_two = ""
        document.getElementById("Bpcross").style.display = "none";
        document.getElementById('second_column').style.display = "none";
      },
      clear_Ainput() {

        document.getElementById("sidebar-search").value = "";
        this.searchterm = ""
        document.getElementById("Apcross").style.display = "none";
        document.getElementById('first_column').style.display = "none";
      },
      first_col_watch(searchterm) { // eslint-disable-line no-unused-vars
        var self = this
        document.getElementById('second_column').style.display = "none";
        if (self.searchterm.length > 0) {
          document.getElementById("Apcross").style.display = "block";
        }
        clearTimeout(self.timeout);

        self.timeout = setTimeout(() => {
          if (self.searchterm.length > 1 && self.searchterm !== "A point on map") {
            document.getElementById('first_column').style.display = "block";
            self.searchset = self.FetchSearchStops(0, self.searchterm);

          } else if (self.searchterm.length == 0 && this.$cookies.get("fromlist").length > 0) {
            document.getElementById('first_column').style.display = "block";
            self.searchset = self.FetchSearchStops(1, this.$cookies.get("fromlist"));
          }
        }, 1000);
      },
      second_col_watch(searchterm_two) { // eslint-disable-line no-unused-vars
        var self = this
        clearTimeout(self.timeout);
        if (self.searchterm_two.length > 0) {
          document.getElementById("Bpcross").style.display = "block";
        }
        self.timeout = setTimeout(() => {
          if (self.searchterm_two.length > 1 && self.searchterm_two !== "A point on map") {
            document.getElementById('second_column').style.display = "block";
            self.searchset_two = self.FetchSearchStops(0, self.searchterm_two);
          } else if (self.searchterm_two.length == 0 && this.$cookies.get("tolist").length > 0) {
            document.getElementById('second_column').style.display = "block";
            self.searchset_two = self.FetchSearchStops(1, this.$cookies.get("tolist"));
          }
        }, 1000);
      },

      fetchAPIData() {
        document.getElementById('find-route').disabled = true;
        document.getElementById("sidebar-search").disabled = true;
        document.getElementById("sidebar-search_two").disabled = true;
        var self = this
        var sp = this.$store.state.startTramStop;
        var ep = this.$store.state.endTramStop;
        var sll = this.$store.state.startPointLatLng;
        var ell = this.$store.state.endPointLatLng;
        var colorcodes = ["#C369F6", "#00c7ba", "#FD0F7E", "#E50C06", "#82DC1F", "#2D45F9"]
        var colorit = 0
        var tt = document.getElementById('stime').value;
        this.$store.state.routeChapterArray = [];
        fetch('/api/v1.0/?' + new URLSearchParams({
            spoint: sp,
            epoint: ep,
            slat: sll[0],
            slong: sll[1],
            elat: ell[0],
            elong: ell[1],
            stime: tt + ':00',
          }))

          .then(response => response.json())
          .then(response => {
            for (var k in response) {
              if (Array.isArray(response[k])) {
                this.$store.state.walkvals = response[k]
              } else {
                if (response[k].line == "walk") {
                  response[k].color = "#808080"
                } else {
                  response[k].color = colorcodes[colorit]
                  colorit += 1
                }
                this.$store.state.routeChapterArray.push(response[k]);
              }
            }
            if (self.searchterm == 'A point on map') {

              this.$store.state.routeChapterArray.unshift({
                "color": this.$store.state.routeChapterArray[0].color,
                "end": "startowakupa",
                "end_time": "11:42",
                "line": "walk",
                "line-pk": 898,
                "line_direction": "Gocławek 06",
                "line_number": 24,
                "start": "Point on map",
                "start_time": this.$store.state.walkvals[2],
                "stopslist": [
                  [this.$store.state.startPointLatLng, "Point on map", "11:38"], this.$store.state.routeChapterArray[0].stopslist[0]
                ],
                "triptime": this.$store.state.walkvals[0]

              })

            }
            if (self.searchterm_two == 'A point on map') {
              this.$store.state.routeChapterArray.push({
                "color": this.$store.state.routeChapterArray.slice(-1)[0].color,
                "end": "Point on map",
                "end_time": this.$store.state.walkvals[3],
                "line": "walk",
                "line-pk": 898,
                "line_direction": "Gocławek 06",
                "line_number": 24,
                "start": this.$store.state.routeChapterArray.slice(-1)[0].end,
                "start_time": this.$store.state.routeChapterArray.slice(-1)[0].end_time,
                "stopslist": [this.$store.state.routeChapterArray.slice(-1)[0].stopslist.slice(-1)[0],
                  [this.$store.state.endPointLatLng, "Point on map", "11:38"]
                ],
                "triptime": this.$store.state.walkvals[1]

              })
            }
            EventBus.$emit('gotAPI');
          })
          .catch(err => {
            console.log(err);
          })
      },

      FetchSearchStops(mode, searchq) {
        let stoparray = [];

        const params = new URLSearchParams('')
        if (mode == 0) {
          params.append('q', searchq)
        } else if (mode == 1) {
          params.append('qs', searchq)
        }

        fetch('/api/v1.0/stops/?' + params)
          .then(response => response.json()
            .then(data => {
              window.data = data;
              Object.values(window.data).forEach(k => {

                stoparray.push(k);

              })
            }))
        return stoparray

      },
      pickStartingPoint(stop) {
        this.$store.state.startTramStop = stop.id;
        this.searchterm = stop.name;
        this.$store.state.startTramStopLatLng = [stop.latitude, stop.longitude];
        EventBus.$emit('setStart');
        document.getElementById('first_column').style.display = "none";
      },
      pickEndingPoint(stop) {
        this.$store.state.endTramStop = stop.id;
        this.searchterm_two = stop.name;
        this.$store.state.stopTramStopLatLng = [stop.latitude, stop.longitude];
        EventBus.$emit('setEnd');
        document.getElementById('second_column').style.display = "none";
      }
    },
  }
  </script>
