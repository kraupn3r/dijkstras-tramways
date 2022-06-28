




<script>
import L from 'leaflet';
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
export default {
  name: "Map",
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
      sharedState: store.state,
      center: [52.233, 21.00],
      markerLatLng: L.latLng(51.504, -0.159),
    }
  },
  mounted() {
    var self = this
    mapObject = self.$refs.mapa.mapObject

 new L.Control.Zoom({ position: 'topright' }).addTo(mapObject);
    self.polylines.addTo(mapObject);
    self.routemarkers.addTo(mapObject);
    self.startsetmarkers.addTo(mapObject);
    self.endsetmarkers.addTo(mapObject);
    self.popuplayer.addTo(mapObject);
    self.routemarkers.clearLayers();



    mapObject.addEventListener('mousemove', function(ev) {
      store.state.mouselatlng = [ev.latlng.lat, ev.latlng.lng]
    });

    //place marker on chosen TramStop's location
    EventBus.$on('setStart', () => {
      self.startsetmarkers.clearLayers();
      self.dropStartMarker(store.state.startTramStopLatLng, self.startsetmarkers)
      mapObject.setView(store.state.startTramStopLatLng, 15);
    });

    EventBus.$on('setEnd', () => {
      self.endsetmarkers.clearLayers();
      self.dropStopMarker(store.state.stopTramStopLatLng, self.endsetmarkers)
      mapObject.setView(store.state.stopTramStopLatLng, 15);
    });



    // Create popupp on right-click at mouse location
    document.getElementById("mapId").addEventListener("contextmenu", function(event) {
      event.preventDefault();
      store.state.pickedLatLng = store.state.mouselatlng
      self.popuplayer.clearLayers();

      var popupContent1 = '<div><div id="butstart"><span class="starticona diricon"></span>set start here</div><div id="butend"><span class="starticonb diricon"></span>set end here</div></div>';

      popup1 = new L.Popup();
      popup1.setLatLng(store.state.pickedLatLng);
      popup1.setContent(popupContent1);
      popup1.addTo(self.popuplayer)
      document.getElementById("butstart").addEventListener("click", function() {
        self.startsetmarkers.clearLayers();
        self.dropStartMarker(store.state.pickedLatLng, self.startsetmarkers);
        EventBus.$emit('pickStartPointLatLng');
        popup1.remove()
        if (self.sharedState.routeChapterArray != null){
          EventBus.$emit('fetchh');
        }
      })
      document.getElementById("butend").addEventListener("click", function() {
        self.endsetmarkers.clearLayers();
        self.dropStopMarker(store.state.pickedLatLng, self.endsetmarkers)

        EventBus.$emit('pickEndPointLatLng');
        popup1.remove()
        if (self.sharedState.routeChapterArray != null){
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
      self.dropStartMarker(store.state.routeChapterArray[0].stopslist[0][0], self.startsetmarkers)



      store.state.routeChapterArray.forEach(el => {
        el.stopslist.forEach(each => {
          var currMarker = L.marker(each[0], {
            icon: icon
          }).setOpacity(0.9).addTo(self.routemarkers);
          currMarker.getElement().style.border = '3px solid ' + el.color;
        })
      })
      store.state.routeChapterArray.forEach(el => {
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


      mapObject.fitBounds(self.polylines.getBounds().pad(1), {
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
