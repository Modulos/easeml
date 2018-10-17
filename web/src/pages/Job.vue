<template>
    <div class="row">
        <div class="col-12">

            <div class="row">
                <div class="col-sm-12">
                    <!-- meta -->
                    <div class="profile-user-box card-box bg-custom">
                        <div class="row">
                            <div class="col-sm-6">

                                <div class="media-body text-white">
                                <span class="pull-left mr-4"><i class="fa fa-cogs thumb-lg" style="font-size: 88px"></i></span>
                                    <!--<h4 class="mt-1 mb-1 font-18">{{job.id}}</h4>-->
                                    <span class="font-13 text-light">
                               
                                    Status: <b>{{job.status}}</b> <br/>
                                    Runtime: <b>{{job.runningDurationString}}</b><br/>
                                    Dataset: <b>{{job.dataset}}</b><br/>
                                    Objective: <b>{{job.objective}}</b>
                                    </span>


                                </div>
                            </div>
                            <div class="col-sm-6">
                                <div class="text-right">
                                    <button type="button" class="btn btn-light waves-effect" :disabled="pauseDisabled" v-show="pauseShow" @click.prevent="pauseClick()">
                                        <i :class="pauseIcon"></i>&nbsp;&nbsp; {{pauseLabel}}
                                    </button>
                                    <button type="button" class="btn btn-light waves-effect" v-show="stopShow" @click.prevent="stopClick()">
                                        <i class="fa fa-stop-circle"></i>&nbsp;&nbsp; Stop
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!--/ meta -->
                </div>
            </div>

            <div class="topgrid card-box">
                <div>
                <h4 class="header-title">Qualities</h4>
                <SumChart ref="summaryPlot"></SumChart>
                     <button class="btn btn-custom waves-light waves-effect" @click.prevent="updatePreviewPlot()">Show Preview</button>
                <PrevChart v-show="showPreview" ref="previewPlot"></PrevChart>
                </div>
                <div>
                <h4 class="header-title">Queued jobs</h4>

                <table class="table table-hover m-0 tickets-list table-actions-bar dt-responsive nowrap" cellspacing="0" width="100%" id="datatable">
                <thead>
                <tr>
                    <th>Model</th>
                    <th>Hyperparameters</th>
                </tr>
                </thead>

                <tbody>
                    <tr v-for="item in combinations" :key="item.id">

                        <td>{{item["modelName"]}}</td>

                        <td>{{item["values"]}}</td>

                    </tr>
                </tbody>
                </table>
                </div>
            </div>



            <div class="card-box">
                

                

                <h4 class="header-title">Job Tasks</h4>

                <table class="table table-hover m-0 tickets-list table-actions-bar dt-responsive nowrap" cellspacing="0" width="100%" id="datatable">
                <thead>
                <tr>
                    <th>
                        ID
                    </th>
                    <th>Model</th>
                    <th>Status</th>
                    <th>Stage</th>
                    <th>Running Time</th>
                    <th>Quality</th>
                    <th>Config</th>
                    <th class="hidden-sm">Action</th>
                </tr>
                </thead>

                <tbody>
                    <tr v-for="item in items" :key="item.intId">

                        <td><b>{{item.intId}}</b></td>

                        <td>{{item.model}}</td>

                        <td>{{item.status}}</td>

                        <td>{{item.stage}}</td>

                        <td>{{ item.runningDurationString }}</td>

                        <td>{{item.quality}}</td>

                        <td>{{item.config}}</td>
                        <td>
                            <button type="button" class="btn btn-icon waves-effect btn-light" v-show="item.status==='completed'" @click.prevent="downloadPredictions(item.id)">
                                <i class="fa fa-cloud-download"></i>
                            </button>
                            <button type="button" class="btn btn-icon waves-effect btn-light" v-show="item.status==='completed'" @click.prevent="downloadTrainedModel(item.id)">
                                <i class="mdi mdi-cube-send"></i>
                            </button>
                        </td>

                    </tr>
                </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import client from "@/client/index"
import SumChart from "@/components/SumChart";
import PrevChart from "@/components/PrevChart";
import tarOpener from "@/schema/tar-opener";
import findReadmeAndScan from "@/modals/NewDataset";
import loadDirectory from "@/schema/src/dataset";
const axios = require('axios');


export default {
    components: {
        SumChart,
        PrevChart
    },
    data() {
        return {
            items: [],
            jobId: "",
            job: {},
            jobModels: null,
            allmodels: [],
            configurations: [],
            modelnames: [],
            stages: {},
            combinations: null,
            configSpace: {},
            showPreview: false,
            datasetItems: null
        };
    },
    computed: {
        pauseLabel() {
            if (this.job.status === "running" || this.job.status === "pausing") {
                return "Pause";
            } else if (this.job.status === "paused" || this.job.status === "resuming") {
                return "Resume";
            } else if (this.job.status === "scheduled") {
                return "Start";
            } else {
                return "[none]";
            }
        },
        pauseIcon() {
            if (this.job.status === "running" || this.job.status === "pausing") {
                return ["fa", "fa-pause-circle"];
            } else if (this.job.status === "paused" || this.job.status === "resuming") {
                return ["fa", "fa-play-circle"];
            } else if (this.job.status === "scheduled") {
                return ["fa", "fa-play-circle"];
            } else {
                return "[none]";
            }
        },
        pauseDisabled() {
            return this.job.status !== "running" && this.job.status !== "paused";
        },
        pauseShow() {
            return ["scheduled", "running", "paused", "pausing", "resuming"].includes(this.job.status);
        },
        stopShow() {
            return ["scheduled", "running", "paused", "pausing", "resuming"].includes(this.job.status);
        }
    },
    methods: {
        openDataset (f) {
            var test = null;
            let n = new numpyReader();
            n.load(f, (array, shape) => {
            // `array` is a one-dimensional array of the raw data
            // `shape` is a one-dimensional array that holds a numpy-style shape.
            console.log(`You loaded an array with ${array.length} elements and ${shape.length} dimensions.`);
            test = array;
            console.log("test npy")
            console.log(test)
            console.log("test npy end")
         })
        },
        updatePreviewPlot () {
            var datasetId = this.datasetItems["0"]["id"]
            console.log(datasetId)
            let context = client.loadContext(JSON.parse(localStorage.getItem("context")));

            context.getDatasetById(datasetId)
            .then(data => {
                console.log(data)
            })
            .catch(e => console.log(e));

            const url = context.axiosInstance.defaults.baseURL + "/datasets/"+datasetId+"/data/train/input/wm4uvjpwmd/vector.ten.npy"
            console.log(url)

            this.openDataset(url)
            //var result = this.openDataset(url)
            //let openerTrainIn = tarOpener.new_opener(result["train"]["input"]);
            //let directory = loadDirectory(url, "", "", openerTrainIn, false);
            //console.log(directory)
            /*// Extract the schema.
            let success = this.extractSchema(result);
            if (success) {
                this.switchStep(+1);
                this.showPreviewOption = true;
            }*/


            this.$refs.previewPlot.updateChart([10, 20, 30, 20, 30]);
            this.showPreview = true;
        },
        allcombs(variants) {
            return (function recurse(keys) {
                if (!keys.length) return [{}];
                let result = recurse(keys.slice(1));
                return variants[keys[0]].reduce( (acc, value) =>
                    acc.concat( result.map( item => 
                        Object.assign({}, item, { [keys[0]]: value }) 
                        ) ),
                    []);})(Object.keys(variants));
        },   
        updateSummaryPlot() {
            this.$refs.summaryPlot.updateChart(this.qualityDict);
        },
        loadData: function() {
            let context = client.loadContext(JSON.parse(localStorage.getItem("context")));

            context.getTasks({job: this.jobId, orderBy: "quality", order: "desc"})
            .then(data => {
                this.items = data;
            })
            .catch(e => console.log(e));

            context.getJobById(this.jobId)
            .then(data => {
                this.job = data;


                // Check if new models have been added to this job.
                if (this.jobModels && this.jobModels.length !== this.job.models.length) {
                    for (let i = 0; i < this.job.models.length; i++) {
                        if (this.jobModels.includes(this.job.models[i]) === false) {
                            // A new model was added to this job. Notify the user.
                            console.log(this.job.models[i]);
                            this.$notify({
                                group: "group",
                                title: "New Model Available",
                                text: "Model <b> \"" + this.job.models[i] + "\" </b> added to this job.",
                                duration: 10000,
                                position: "bottom right",
                                type: "warn"
                            });
                        }
                    }
                }
                if (this.job.models && this.modelnames.length != this.job.models.length) {
                    for (let i = 0; i < this.job.models.length; i++) {
                        if (this.modelnames.includes(this.job.models[i]) === false) {
                            this.modelnames.push(this.job.models[i]);
                            this.qualityDict[this.job.models[i]] = [];
                        }
                    }
                }

                this.jobModels = this.job.models;
                
                for (var i=0; i<this.items.length; i++) {
                    if (this.configurations.includes(this.items[i].intId) === false) {
                        this.configurations.push(this.items[i].intId);
                        this.stages[this.items[i].intId] = false;
                    }
                    if ((this.items[i].stage == "end")&&(this.stages[this.items[i].intId] === false)) {
                        this.stages[this.items[i].intId] = true;
                        this.qualityDict[this.items[i].model].push(this.items[i].quality);
                    }
                }
                this.updateSummaryPlot();
                
            })
            .catch(e => console.log(e));

            context.getDatasets().then(data => {this.datasetItems = data;})
        
        },
        pauseClick() {

            let context = client.loadContext(JSON.parse(localStorage.getItem("context")));

            let newStatus = null;
            if (this.job.status === "running") {
                newStatus = "pausing";
            } else if (this.job.status === "paused") {
                newStatus = "resuming";
            } else if (this.job.status === "scheduled") {
                newStatus = "running";
            }

            if (newStatus) {
                context.updateJob(this.jobId, {"status" : newStatus})
                this.job.status = newStatus;
            }

        },
        stopClick() {

            let context = client.loadContext(JSON.parse(localStorage.getItem("context")));

            let newStatus = null;
            if (["scheduled", "running", "paused", "pausing"].includes(this.job.status)) {
                context.updateJob(this.jobId, {"status" : "terminating"})
                this.job.status = "terminating";
            }

        },
        downloadPredictions: function(taskId) {
            let context = client.loadContext(JSON.parse(localStorage.getItem("context")));

            context.downloadTaskPredictionsByPath(taskId, ".tar", true)
        },
        downloadTrainedModel: function(taskId) {
            let context = client.loadContext(JSON.parse(localStorage.getItem("context")));

            context.downloadTrainedModelAsImage(taskId, true)
        }
    },
    mounted() {if (!(this.combinations)) {
        var combId = 0;
        this.combinations = [];
        let context = client.loadContext(JSON.parse(localStorage.getItem("context")));
         context.getModules({
                type: "model",
                status: "active"
            }).then(data => {
                this.allmodels = data;
                this.selectedModels = this.allmodels;
                console.log(this.allmodels);
                for(var mid in this.allmodels){
                    var midstr = this.allmodels[mid].id;
                    var tmpConfig = JSON.parse(this.allmodels[mid]["configSpace"]);
                    this.configSpace[midstr] = {};
                    for (var paramName in tmpConfig) {
                        var tmpSubConfig = tmpConfig[paramName][".choice"];
                        var tmpValues = [];
                        for (var subkey in tmpSubConfig) {
                            tmpValues.push(tmpSubConfig[subkey])
                        }
                        this.configSpace[midstr][paramName] = tmpValues;
                    }
                    let tmpCombs = this.allcombs(this.configSpace[midstr]);
                    //console.log(tmpCombs);
                    for (var tmpCombsKey in tmpCombs) {
                        this.combinations.push({"id": combId, "modelName": midstr, "values": tmpCombs[tmpCombsKey]});
                        combId = combId + 1;
                    }
                    
                }
                })
        }

        this.qualityDict = {};
        this.jobId = this.$route.params.id;
        this.loadData();
        
        // Repeat call every 1 second.
        this.timer = setInterval(function() {
            this.loadData();
        }.bind(this), 5000);
    },
    beforeDestroy() {
        clearInterval(this.timer);
    }
};
</script>
<style>
    .info {
        height: 700px;
        overflow: auto;
    }
    .topgrid{
        height: 350px;
        overflow: auto;
        display: grid;
        grid-gap: var(--spacing);
        grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
        min-height: calc(100vh - var(--spacing)*2);
    }
</style>
