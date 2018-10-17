<template>
<modal name="inspect-job-task" transition="pop-out" height="900" width="1000" @before-open="mounted">

        <button type="button" class="close" onclick="">
            <span>&times;</span><span class="sr-only">Close</span>
        </button>
        <h4 class="custom-modal-title">Inspect Job Task</h4>
        <div class="custom-modal-text">
            <form class="form-horizontal" action="#">

                <div class="wiz-container">
                    <transition name="fade" mode="out-in">
                        <div class="row">
                            <div class="col-6">
                                <div>
                                    <h4>Job details</h4>
                                    <ul>
                                    <li>Status: {{items[0].status}}</li>
                                    <li>Running duration: {{items[0].runningDurationString}}</li>
                                    <li>Quality: {{items[0].quality}}</li>
                                    <li>Expected quality: {{items[0].qualityExpected}}</li>
                                    </ul>
                                </div>
                                <div>
                                    <h4>Hyperparameter settings</h4>
                                    <ul>
                                    <li v-for="(value, key) in JSON.parse(items[0].config)" v-bind:key="key">
                                        <span>{{key}}: {{value}}</span>
                                    </li>
                                    </ul>
                                </div>
                                <div>
                                    <div v-if="objective !== null">
                                        <h4>Objective: {{objective.name}}</h4>
                                        <span v-html="ObjectiveDescriptionHtml"></span>
                                    </div>
                                </div>
                                <div>
                                    <div v-if="objective !== null">
                                        <h4>Model: {{model.name}}</h4>
                                        <span v-html="ModelDescriptionHtml"></span>
                                    </div>
                                </div>
                                
                            </div>
                            <div class="col-6">
                                <div>
                                    <h4>Training dataset</h4>
                                </div>
                                <div>
                                    <h4>Test dataset</h4>
                                </div>
                            </div>
                        </div>
                    </transition>
                </div>
            </form>
        </div>
    </modal>
</template>

<script>
import client from "@/client/index";
import showdown from "showdown";
var converter = new showdown.Converter();

export default {
    data() {
        return {
            items: [],
            jobId: "",
            job: {},
            jobModels: null,
            model: [],
            slectedModels: [],
            objective: [],
        };
    },
    computed: {
        ModelDescriptionHtml() {
            if(this.model  !== null){
                return converter.makeHtml(this.model.description);
            } else {
                return ""
            }
        },
        ObjectiveDescriptionHtml() { 
            if (this.objective !== null){
                return converter.makeHtml(this.objective.description);
            } else {
                return ""
            }
        },
    },
    methods: {
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
                this.jobModels = this.job.models;
            })
            .catch(e => console.log(e));

            context.getModuleById(this.jobModels)
            .then(data => {
                this.model = data;
            })
            .catch(e => console.log(e));

            context.getModules({type: "objective"})
            .then(data => {
                for (var obj in data){
                    if (data[obj].id === this.items[0].objective){
                        this.objective = data[obj]
                    };
                };
            })
            .catch(e => console.log(e));
        },
    },
    mounted() {

        this.jobId = this.$route.params.id;
        this.loadData();
        
        // Repeat call every 1 second.
        this.timer = setInterval(function() {
            this.loadData();
        }.bind(this), 1000);
    },
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.wiz-container {
    position: relative;
    height: 420px;
}
.wiz-step {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
}
.wiz-buttons {
    text-align: right;
    vertical-align: bottom;
}
.close {
    margin: 15px;
}
</style>