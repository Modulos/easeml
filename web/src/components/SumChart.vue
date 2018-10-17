<template>
  <div class="example">
    <apexcharts width="400" height="250" type="line" :options="chartOptions" :series="series"></apexcharts>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: 'SumChart',
  components: {
    apexcharts: VueApexCharts,
  },
  data: function() {
    return {
      chartOptions: {
        markers: {
        size: 0,
        style: 'full',
      },stroke: { 
      width: 2
    }
      },
      series: []
  }
},
   methods: {
       find_index(s, k) {
           var res = null;
           for (let i =0;i<s.length;i++) {
               if (s[i]["name"] === k) {
                   res = i
               }
           }
           return res;
       },
      updateChart(newDataDict) {
        var names = [];
        for (var i=0;i<this.series.length;i++) {
            if (names.includes(this.series[i]["name"]) === false) {
                names.push(this.series[i]["name"]);
            }
        }
        for (var key in newDataDict) {
            if (names.includes(key) == false) {
                this.series.push({name: key, data: newDataDict[key]})
            } else {
                var index = this.find_index(this.series, key)
                this.series[index]["data"] = newDataDict[key];
            }
        }

      }
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

