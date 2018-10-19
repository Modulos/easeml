<template>
<modal name="inspect-job-task" transition="pop-out" height="auto" width="1000" @before-open="beforeOpen"> 

        <button type="button" class="close" @click="$modal.hide('inspect-job-task')">
            <span>&times;</span><span class="sr-only">Close</span>
        </button>

        <h4 class="custom-modal-title">Inspect Job Task</h4>
        <div class="custom-modal-text">
            <form class="form-horizontal" action="#">

                <div :class="wizContainerClasses">

                    <transition name="fade" mode="out-in">
                        <div class="row">
                            <div class="col-6">
                                <div>
                                    <h4>Job details</h4>
                                    <ul>
                                    <li>Status: {{items.status}}</li>
                                    <li>Running duration: {{items.runningDurationString}}</li>
                                    <li>Quality: {{items.quality}}</li>
                                    <li>Expected quality: {{items.qualityExpected}}</li>
                                    </ul>
                                </div>
                                <div>
                                    <h4>Hyperparameter settings</h4>
                                    <ul v-if="items.config">
                                    <li v-for="(value, key) in JSON.parse(items.config)" v-bind:key="key">
                                        <span>{{key}}: {{value}}</span>
                                    </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col-6">
                                <div>
                                    <div v-if="thisobjective">
                                        <h4>Objective: {{thisobjective.name}}</h4>
                                        <span v-html="ObjectiveDescriptionHtml"></span>
                                    </div>
                                </div>
                                <div>
                                    <div v-if="thismodel">
                                        <h4>Model: {{thismodel.name}}</h4>
                                        <span v-html="ModelDescriptionHtml"></span>
                                    </div>
                                </div>
                                <!--
                                <div>
                                    <h4>Training dataset</h4>
                                    <PrevChart v-show="showPreview" ref="previewPlot"></PrevChart>
                                </div>
                                <div>
                                    <h4>Test dataset</h4>
                                </div>-->
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
import PrevChart from "@/components/PrevChart";
import showdown from "showdown";
var converter = new showdown.Converter();

export default {
    data() {
        return {
            items: [],
            jobId: "",
            allmodels: [],
            allobjectives: [],
            thismodel: null,
            thisobjective: null,
            inputdata: [],
            showPreview: false,
        };
    },
    computed: {
        ModelDescriptionHtml() {
            if(this.thismodel){
                return converter.makeHtml(this.thismodel.description);
            } else {
                return ""
            }
        },
        ObjectiveDescriptionHtml() { 
            if (this.thisobjective){
                return converter.makeHtml(this.thisobjective.description);
            } else {
                return ""
            }
        },
    },
    methods: {
        beforeOpen(event) {

            this.items = event.params.item;
            this.allmodels = event.params.allmodels;
            this.allobjectives = event.params.allobjectives;
            // this.inputdata = event.params.inputdata;

            for(var m in this.allmodels){
                if (this.allmodels[m].id === this.items.model){
                    this.thismodel = this.allmodels[m]
                }
            };

            for(var o in this.allobjectives){
                if (this.allobjectives[o].id === this.items.objective){
                    this.thisobjective = this.allobjectives[o]
                }
            };
            // console.log(this.inputdata);
            // this.$refs.previewPlot.updateChart(this.inputdata);
            // this.showPreview = true;
        },
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