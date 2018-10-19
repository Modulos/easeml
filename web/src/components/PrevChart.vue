<template>
  <div class="example">
    <apexcharts width="450" height="250" type="line" :options="chartOptions" :series="series"></apexcharts>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: 'PrevChart',
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
      series: [{
        name: 'series-1',
        data: []
      }]
  }
},
   methods: {
      updateChart(newData) {
        this.series = [{
          data: newData
        }]

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
