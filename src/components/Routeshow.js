<template>
<div id="routeshowContainer" >
<div class="routeHeader">
<div class="routeHeaderLeft"><div id="timec" v-if="starttrip < 60 && starttrip > 0" class="timewrapper">starts in:<div > <div class="timediv shineanim">{(starttrip)}</div> min</div></div><div v-else-if="starttrip < 1" id="departed"><div>departed</div> <div>:(</div></div>
<div v-else class="timewrapper">start at:<div > <div class="timediv">{(this.startime)}</div></div></div></div>

<div class="routeHeaderRight">
<div class="routeVehicles">
<div class="vforicons" v-for="each in content">

<div class="vif" v-if="each.line != 'walk'" v-bind:style="{'border-bottom':' 2px solid '+each.color}">
<div class="iconWrapper"><div class="tramIcon" ></div></div>
<div class="aftericon">{(each.line_number)}</div>
</div>
</div>
<div class="totaltime">{(this.trippTime)} min</div></div>
<div class="timeline">
 <div ><div class="divinline" v-for="e in content" v-if="e ===content[0] && e.triptime > 0 && e.line === 'walk'"><div class="walkIcon"></div><div class="aftericon">{(e.triptime)} min</div></div><span class="timess">{(this.startime)} - {(this.endtime)}</span><div class="divinline" v-for="e in content" v-if="e ===content[content.length-1] && e.triptime > 0  && e.line === 'walk'"><div class="walkIcon"></div><div class="aftericon">{(e.triptime)} min</div></div></div>
</div>
</div>

</div>
<div class="routeTable">
<table>
<tbody v-for="each,index in content" >
<tr >
<td><div class="chapterTime"><div v-if="each == content[0]" class="starticona clasleft"></div><span>{(each.start_time)}</span></div></td>
<td>{(each.start)}</td>
</tr>
<tr >
<td class="vehicleBar" v-if="each.line == 'walk'" ><div v-bind:style="{ 'background-color': '#A0A0A0'}" class="chapterVehicle"><div class="iconWrapper"> <div  class="walkIcon"></div></div></div></td>
  <td class="vehicleBar" v-else ><div v-bind:style="{ 'background-color': each.color }" class="chapterVehicle"><div class="iconWrapper">  <div class="tramIcon"></div><div class="aftertram">{(each.line_number)}</div></div></div></td>

  <td v-if="each.line == 'walk'"><div class="chapterLineInfo"><div></div><div>{(each.triptime)} min</div></div></td>
<td v-else-if="each.line != 'walk'"> <div class="chapterLineInfo"> <div>Direction: {(each.line_direction)}</div><div>{(each.triptime)} min</div></div><div class="openstops"><div class="clickable " :id="'open'+index" @click="openStops(index)">{(each.stopslist.length)} stops</div><div class="stoplist clickable" @click="closeStops(index)" :id="index" style="display:none;"><div v-for="leach in each.stopslist">{(leach[2])} {(leach[1])}</div></div></div></td>
</tr>
<tr class="lastbar" >
<td><div class="chapterTime"><div v-if="each == content[content.length-1]" class="starticonb clasleft"></div><span>{(each.end_time)}</span></div></td>
<td>{(each.end)}</td>
</tr>
</tbody>
</table>
</div>

</div>
</template>



export default {
  name: "Routeshow",
  delimiters: ['{(', ')}'],
  data: () => {
    return {
      sharedState: store.state,
      content: null,
      trippTime: 0,
      startime: 0,
      endtime: 0,
      starttrip: null,
      interval: null,
      currtime: null,
      lasttime: null,
    }
  },
  mounted() {
    self = this
    document.getElementById('routeshowContainer').style.display = "none";

    EventBus.$on('timesup', () => {
      clearInterval(self.interval)


    })
    EventBus.$on('gotAPI', () => {
      self.trippTime = store.state.walkvals[4]
      self.starttrip = store.state.walkvals[6]
      document.getElementById('routeshowContainer').style.display = "block";
      self.content = store.state.routeChapterArray;

      self.startime = self.content[0].start_time
      self.endtime = self.content[self.content.length - 1].end_time
      self.lasttime = Intl.DateTimeFormat(navigator.language, {
        minute: 'numeric',
      }).format()
      clearInterval(self.interval)
      self.interval = setInterval(() => {
        // Concise way to format time according to system locale.
        // In my case this returns "3:48:00 am"
        self.currtime = Intl.DateTimeFormat(navigator.language, {
          minute: 'numeric',
        }).format()
        if (self.currtime != self.lasttime && self.starttrip > 0) {
          self.lasttime = self.currtime;
          self.starttrip -= 1;
        }
        else if (self.starttrip == 0){
          EventBus.$emit('timesup');
        }
      }, 5000)
    })
  },

  methods: {
    pickMarker(marker) {
      EventBus.$emit('pickMarker', marker);
    },
    openStops(index) {
      document.getElementById(index).style.display = "block";

      document.getElementById('open' + index).style.display = "None";
    },
    closeStops(index) {
      document.getElementById(index).style.display = "None";

      document.getElementById('open' + index).style.display = "block";
    }
  },


}
