<template>
    <v-content color="primary" v-if="$store.getters.isSuperuser">
        <v-snackbar
                v-model="snackbar"
                :timeout="timeout"
                top
        >
            {{ t(text) }}
            <v-btn
                    flat
                    @click="snackbar = false"

            >
                {{t('Close')}}
            </v-btn>
        </v-snackbar>
        <v-container fluid id="main-container" grid-list-md>
            <v-layout row wrap>
                <v-flex md12 class="mt-3">
                    <v-tabs
                            color="primary"
                            dark
                    >
                        <v-tab>{{t('This month')}}</v-tab>
                    </v-tabs>
                </v-flex>
                <!--<v-flex md2>-->
                <!--<v-btn depressed small color="primary">+ Lead</v-btn>-->
                <!--</v-flex>-->
                <v-flex xs12 md3 justify-center>
                    <chart-info
                            :data="mainStat.carriers"
                            :name="t('Carriers')"
                    />
                </v-flex>
                <v-flex xs12 md3 justify-center>
                    <chart-info
                            :data="mainStat.closed_leads"
                            :name="t('Closed leads')"
                    />
                </v-flex>
                <v-flex xs12 md3 justify-center>
                    <chart-info
                            :data="mainStat.closed_orders"
                            :name="t('Completed orders')"
                    />
                </v-flex>
                <v-flex xs12 md3 justify-center>
                    <chart-info
                            :data="mainStat.opened_leads"
                            :name="t('Open leads')"
                    />
                </v-flex>
                <v-flex md12 class="mt-3">
                    <v-tabs
                            color="primary"
                            dark
                            class="tabs-fix"
                    >
                        <v-tab @click="getDataPeriod(0)">{{t('All time')}}</v-tab>
                        <v-tab @click="getDataPeriod(1)">{{t('Last month')}}</v-tab>
                        <v-tab @click="getDataPeriod(2)">{{t('Three month')}}</v-tab>
                        <v-tab @click="getDataPeriod(3)">{{t('This year')}}</v-tab>
                    </v-tabs>
                </v-flex>
                <v-flex xs12 md3 justify-center>
                    <chart-info
                            :data="secondStat.carriers"
                            :name="t('Carriers')"
                    />
                </v-flex>
                <v-flex xs12 md3 justify-center>
                    <chart-info
                            :data="secondStat.closed_leads"
                            :name="t('Closed leads')"
                    />
                </v-flex>
                <v-flex xs12 md3 justify-center>
                    <chart-info
                            :data="secondStat.closed_orders"
                            :name="t('Completed orders')"
                    />
                </v-flex>
                <v-flex xs12 md3 justify-center>
                    <chart-info
                            :data="secondStat.opened_leads"
                            :name="t('Open leads')"
                    />
                </v-flex>
            </v-layout>
            <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <v-btn
                            color="accent"
                            light
                            fixed
                            bottom
                            left
                            fab
                            v-on="on"
                            to="/leads/create"
                    >
                        <v-icon color="dark">add</v-icon>
                    </v-btn>
                </template>
                <span>{{t('Add lead')}}</span>
            </v-tooltip>
        </v-container>

    </v-content>
    <v-tooltip right v-else>
        <template v-slot:activator="{ on }">
            <v-btn
                    color="accent"
                    light
                    fixed
                    bottom
                    left
                    fab
                    v-on="on"
                    to="/leads/create"
            >
                <v-icon color="dark">add</v-icon>
            </v-btn>
        </template>
        <span>{{t('Add lead')}}</span>
    </v-tooltip>
</template>

<script>
    import axios from "axios";
    import ChartInfo from "../../components/Charts/ChartInfo";


    export default {
        name: "Dashboard",
        components: {ChartInfo},
        data() {
            return {
                secondStat: {
                    carriers: {value: 0},
                    closed_leads: {value: 0},
                    closed_orders: {value: 0},
                    opened_leads: {
                        value: 0
                    },

                },
                mainStat: {
                    carriers: {value: 0},
                    closed_leads: {value: 0},
                    closed_orders: {value: 0},
                    opened_leads: {
                        value: 0
                    },
                },
                snackbar: false,
                text: 'Oops... Something went wrong',
                timeout: 5000,
            }
        },
        computed: {},
        methods: {
            getData() {
                axios.get(`${this.$hostname}/api/dashboard/`)
                    .then((response) => {
                        console.log(response.data)
                        if (response.status === 200) {
                            this.mainStat = response.data
                        }
                    }).catch((error) => {
                    this.text = "Connection error";
                    console.log(error)
                    this.snackbar = true;
                });
            },
            getDataPeriod(type=0) {
                axios.post(`${this.$hostname}/api/dashboard/`, {type: type})
                    .then((response) => {
                        console.log(response.data)
                        if (response.status === 200) {
                            this.secondStat = response.data
                        }
                    }).catch((error) => {
                    this.text = "Connection error";
                    console.log(error)
                    this.snackbar = true;
                });
            },
        },
        mounted() {
            this.getData();
            this.getDataPeriod();
        },
        beforeCreate() {
            if (!this.$session.exists()) {
                this.$router.push('/')
            }
        },
    }

</script>

<style lang="scss">
    .apexcharts-toolbar, .apexcharts-tooltip {
        z-index: 2 !important;
    }
    @media only screen and (max-width: 768px) {
       .v-tabs__container{
            display: block;
            height: 100%
        }
        .v-tabs__div{
            display: flex;
            height: 30px;
            padding-left: 150px
        }
    }
</style>