<template>
  <div class="box">
<vuescrollingtable :scroll-vertical="scrollVertical" :scroll-horizontal="scrollHorizontal">
  <template slot="thead">
    <tr>
    <th v-for="col in gridColumns" :key="col">{{ col }}</th>
    </tr>
  </template>
  <template slot="tbody">
    <tr v-for="item in gridData" :key="item">
    <td v-for="col in gridColumns" :key="col">
    {{ item[col] }}
  </td>
    </tr>
  </template>
</vuescrollingtable>
</div>
</template>

<script>

import VueScrollingTable from 'vue-scrolling-table'
export default {
  name: 'PreviewTable',
  components: {
    vuescrollingtable: VueScrollingTable,
  },
  props: {
    data: Array,
    columns: Array
  },
  data: function () {
    return {
      gridColumns: ['time', 'feature1'],
      gridData: [
      { time: '0', feature1: Infinity },
      { time: '1', feature1: 9000 },
      { time: '2', feature1: 7000 },
      { time: '3', feature1: Infinity },
      { time: '4', feature1: 9000 },
      { time: '5', feature1: 7000 },
      { time: '0', feature1: Infinity },
      { time: '1', feature1: 9000 },
      { time: '2', feature1: 7000 },
      { time: '3', feature1: Infinity },
      { time: '4', feature1: 9000 },
      { time: '5', feature1: 7000 },
      { time: '0', feature1: Infinity },
      { time: '1', feature1: 9000 },
      { time: '2', feature1: 7000 },
      { time: '3', feature1: Infinity },
      { time: '4', feature1: 9000 },
      { time: '5', feature1: 7000 },
      { time: '0', feature1: Infinity },
      { time: '1', feature1: 9000 },
      { time: '2', feature1: 7000 },
      { time: '3', feature1: Infinity },
      { time: '4', feature1: 9000 },
      { time: '5', feature1: 7000 },
      { time: '6', feature1: 8000 }
      ]
    }
  },
  methods: {
    updateEntries (newData) {
      var items = [];
      var minidict;
      for (var index = 0; index < newData.length; index++) {
        minidict = [];
        minidict.push({
          key: "time",
          value: newData[index][0]
        });
        minidict.push({
          key: "feature1",
          value: newData[index][1]
        })
        items.push(minidict)
      }

      this.items = [{
          gridData: items
        }]
    }
  }
}


</script>

<style scoped>
.box {
  clear: both;
  padding: 0;
  height: 210px;
  margin-left: auto;
  margin-right: auto;
  overflow: hidden;
}
th {
  background-color: #2d7bf4;
  /*color: rgba(255,255,255,0.66);*/
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
td {
  background-color: #f9f9f9;
}

th, td {
  padding: 10px 10px;
}
</style>
