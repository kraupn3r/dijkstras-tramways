<template>

    <l-map ref='mapa' id="mapId" @click="mouseOut" style="height: 100%" :options="{ zoomControl: false }" :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker :lat-lng="markerLatLng"></l-marker>
    </l-map>
</template>




<script>
import { EventBus } from "../main";
import L from 'leaflet';
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";


  var icon = L.divIcon({
    className: 'map-marker',
    iconSize: [10, 10],

  });
  var bigicon = L.divIcon({
    className: 'map-markerbig',
    iconSize: [23, 23],


  });
  var bigendicon = L.divIcon({
    className: 'map-markerend',
    iconSize: [23, 23],

});


export default {
  name: "Map", // eslint-disable-line vue/multi-word-component-names
  components: {
    "l-map": LMap,
    "l-tile-layer": LTileLayer,
    LMarker
  },
  data() {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 13,
      polylines: L.featureGroup(),
      routemarkers: L.featureGroup(),
      startsetmarkers: L.featureGroup(),
      endsetmarkers: L.featureGroup(),
      popuplayer: L.featureGroup(),
      sharedState: this.$store.state,
      center: [52.233, 21.00],
      markerLatLng: L.latLng(51.504, -0.159),
    }
  },
  mounted() {
    var self = this
    delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});
    self.mapObject = self.$refs.mapa.mapObject;
 new L.Control.Zoom({ position: 'topright' }).addTo(self.mapObject);
    self.polylines.addTo(self.mapObject);
    self.routemarkers.addTo(self.mapObject);
    self.startsetmarkers.addTo(self.mapObject);
    self.endsetmarkers.addTo(self.mapObject);
    self.popuplayer.addTo(self.mapObject);
    self.routemarkers.clearLayers();



    self.mapObject.addEventListener('mousemove', function(ev) {
      self.$store.state.mouselatlng = [ev.latlng.lat, ev.latlng.lng]
    });

    //place marker on chosen TramStop's location
    EventBus.$on('setStart', () => {
      self.startsetmarkers.clearLayers();
      self.dropStartMarker(self.$store.state.startTramStopLatLng, self.startsetmarkers)
      self.mapObject.setView(self.$store.state.startTramStopLatLng, 15);
    });

    EventBus.$on('setEnd', () => {
      self.endsetmarkers.clearLayers();
      self.dropStopMarker(self.$store.state.stopTramStopLatLng, self.endsetmarkers)
      self.mapObject.setView(self.$store.state.stopTramStopLatLng, 15);
    });



    // Create popupp on right-click at mouse location
    document.getElementById("mapId").addEventListener("contextmenu", function(event) {
      event.preventDefault();
      self.$store.state.pickedLatLng = self.$store.state.mouselatlng
      self.popuplayer.clearLayers();

      var popupContent1 = '<div><div id="butstart"><span class="starticona diricon"></span>set start here</div><div id="butend"><span class="starticonb diricon"></span>set end here</div></div>';

      var popup1 = new L.Popup();
      popup1.setLatLng(this.$store.state.pickedLatLng);
      popup1.setContent(popupContent1);
      popup1.addTo(self.popuplayer)
      document.getElementById("butstart").addEventListener("click", function() {
        self.startsetmarkers.clearLayers();
        self.dropStartMarker(self.$store.state.pickedLatLng, self.startsetmarkers);
        EventBus.$emit('pickStartPointLatLng');
        popup1.remove()
        if (self.sharedState.routeChapterArray != null){
          EventBus.$emit('fetchh');
        }
      })
      document.getElementById("butend").addEventListener("click", function() {
        self.endsetmarkers.clearLayers();
        self.dropStopMarker(self.$store.state.pickedLatLng, self.endsetmarkers)

        EventBus.$emit('pickEndPointLatLng');
        popup1.remove()
        if (self.$store.routeChapterArray != null){
          EventBus.$emit('fetchh');
        }
      })
      return false;
    })


    EventBus.$on('gotAPI', () => {
      document.getElementById('find-route').disabled = false;
      document.getElementById('sidebar-search').disabled = false;
      document.getElementById('sidebar-search_two').disabled = false;
      self.routemarkers.clearLayers();
      self.polylines.clearLayers();
      self.startsetmarkers.clearLayers();
      self.dropStartMarker(self.$store.state.routeChapterArray[0].stopslist[0][0], self.startsetmarkers)



      self.$store.state.routeChapterArray.forEach(el => {
        el.stopslist.forEach(each => {
          var currMarker = L.marker(each[0], {
            icon: icon
          }).setOpacity(0.9).addTo(self.routemarkers);
          currMarker.getElement().style.border = '3px solid ' + el.color;
        })
      })
      this.$store.state.routeChapterArray.forEach(el => {
        if (el.line == "walk") {
          L.polyline(el.stopslist.map(x => x[0]), {
            color: "#808080",
            dashArray: 4,
            opacity: 0.9
          }).addTo(self.polylines);
        } else {

          L.polyline(el.stopslist.map(x => x[0]), {
            color: el.color,
            weight: 6,
            opacity: 0.9

          }).addTo(self.polylines);
        }
      })


      self.mapObject.fitBounds(self.polylines.getBounds().pad(1), {
        maxZoom: 13
      });
    });

  },

  methods: {
    dropStartMarker(position, layer) {
      var startMarker = L.marker(position, {
        icon: bigicon
      }).addTo(layer)
      startMarker.setZIndexOffset(1000);
      startMarker.getElement().style.backgroundColor = "white";

    },
    dropStopMarker(position, layer) {
      var stopMarker = L.marker(position, {
        icon: bigendicon
      }).addTo(layer)
      stopMarker.setZIndexOffset(1000);
      stopMarker.getElement().style.backgroundColor = 'white';
    },
    mouseOut() {
      document.getElementById('first_column').style.display = "none";
      document.getElementById('second_column').style.display = "none";
    }
  }
}
</script>
