<template>
    <v-content color="primary">
        <v-container fluid id="main-container" grid-list-md fill-height>
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
            <v-layout
                    justify-center
                    wrap
            >
                <v-flex xs12>
                    <v-card
                            class="mx-auto"
                            :loading="loading"
                    >
                        <v-form ref="form" @submit.prevent="createLead">
                            <v-container>
                                <v-layout row wrap>
                                    <v-flex
                                            xs12
                                            md4
                                    >
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('First name')"
                                                type="text"
                                                :rules="[rules.required]"
                                                v-model="details.name_client"></v-text-field>
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('Last name')"
                                                type="text"
                                                v-model="details.surname_client"></v-text-field>
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('Phone')"
                                                type="tel"
                                                :rules="[rules.required, rules.phone]"
                                                v-model="details.phone"></v-text-field>
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('Email')"
                                                type="email"
                                                :rules="[rules.email]"
                                                v-model="details.email"></v-text-field>
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('Transportation cost')"
                                                min="0"
                                                :rules="[rules.intNumber]"
                                                v-model="details.transportation_cost"></v-text-field>
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('Lead cost')"
                                                min="0"
                                                :rules="[rules.required, rules.intNumber]"
                                                v-model="details.lead_cost"></v-text-field>
                                        <v-checkbox
                                                    class="mr-0 mr-md-3"
                                                    v-model="details.hot"
                                                    :label="t('Hot lead')"
                                                    color="primary"

                                        ></v-checkbox>
                                    </v-flex>
                                    <v-flex
                                            xs12
                                            md4
                                    >
                                        <v-select
                                                v-model="details.region"
                                                :items="regions"
                                                item-text="region"
                                                item-value="pk"
                                                :label="t('Region')"
                                                data-vv-name="select"
                                                :disabled="edit"
                                                :rules="[rules.required]"
                                        ></v-select>
                                        <v-select
                                                v-model="details.type_car"
                                                :items="typeCars"
                                                item-text="type_car"
                                                item-value="pk"
                                                :label="t('Type car')"
                                                data-vv-name="select"
                                                :disabled="edit"
                                        ></v-select>
                                        <v-textarea
                                                :label="t('text')"
                                                :disabled="edit"
                                                v-model="details.text"
                                                :rules="[rules.comment]"
                                        ></v-textarea>
                                        <v-select
                                                v-model="details.type_transport"
                                                :items="typeTransport"
                                                item-text="type_transport"
                                                item-value="pk"
                                                :label="t('Type transport')"
                                                data-vv-name="select"
                                                :disabled="edit"
                                        ></v-select>
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('Address from')"
                                                type="text"
                                                v-model="details.address_from"></v-text-field>
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('From city')"
                                                :rules="[rules.required]"
                                                v-model="details.city_from"></v-text-field>
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('Address to')"
                                                type="text"
                                                v-model="details.address_to"></v-text-field>
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('To city')"
                                                :rules="[rules.required]"
                                                v-model="details.city_to"></v-text-field>
                                        <v-text-field
                                                v-model="details.date"
                                                :label="t('Date')"
                                                class="mr-0 mr-md-3"
                                        ></v-text-field>
                                        <v-text-field
                                                :disabled="edit"
                                                v-model="details.time"
                                                :label="t('Time')"
                                                style="direction: rtl"
                                                class=""
                                        ></v-text-field>
                                    </v-flex>
                                    <v-flex
                                            xs12
                                            md4
                                    >
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('Stages from')"
                                                :rules="[rules.required]"
                                                v-model="details.floor_from"></v-text-field>
                                        <v-radio-group row>
                                            <v-checkbox
                                                    class="mr-0 mr-md-3"
                                                    v-model="details.first_crane"
                                                    :label="t('crane')"
                                                    color="primary"

                                            ></v-checkbox>
                                            <v-checkbox
                                                    class="mr-0 mr-md-3"
                                                    v-model="details.first_lift"
                                                    :label="t('lift')"
                                                    color="primary"

                                            ></v-checkbox>
                                            <v-checkbox
                                                    class="mr-0 mr-md-3"
                                                    v-model="details.first_entryway"
                                                    :label="t('entryway')"
                                                    color="primary"

                                            ></v-checkbox>
                                        </v-radio-group>
                                        <v-text-field
                                                class="mr-0 mr-md-3"
                                                :label="t('Stages to')"
                                                :rules="[rules.required]"
                                                v-model="details.floor_to"></v-text-field>
                                        <v-radio-group row>
                                            <v-checkbox
                                                    class="mr-0 mr-md-3"
                                                    v-model="details.second_crane"
                                                    :label="t('crane')"
                                                    color="primary"

                                            ></v-checkbox>
                                            <v-checkbox
                                                    class="mr-0 mr-md-3"
                                                    v-model="details.second_lift"
                                                    :label="t('lift')"
                                                    color="primary"

                                            ></v-checkbox>
                                            <v-checkbox
                                                    class="mr-0 mr-md-3"
                                                    v-model="details.second_entryway"
                                                    :label="t('entryway')"
                                                    color="primary"

                                            ></v-checkbox>
                                        </v-radio-group>
                                        <v-radio-group v-model="details.category" row>
                                            <v-radio
                                                    :label="t('Open lead')"
                                                    :value="false"
                                                    color="primary"
                                            ></v-radio>
                                            <v-radio
                                                    :label="t('Closed lead')"
                                                    :value="true"
                                                    color="primary"
                                            ></v-radio>
                                        </v-radio-group>

                                    </v-flex>
                                </v-layout>
                            </v-container>
                            <v-flex xs12>
                                <v-textarea
                                        :label="t('Comment')"
                                        class="mx-4"
                                        v-model="details.comment"
                                        :rules="[rules.comment]"
                                ></v-textarea>
                            </v-flex>
                            <v-flex
                                    xs12
                                    class="d-flex justify-content-end"
                            >

                                <div style="flex: initial !important;" class="ml-auto">
                                    <v-btn small color="primary" type="submit">
                                        {{t('Save')}}
                                    </v-btn>

                                </div>
                            </v-flex>

                        </v-form>

                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </v-content>
</template>

<script>
    import axios from 'axios';
    import  mask  from 'vue-the-mask'

    export default {
        name: "LeadsCreate",
        data() {
            return {
                edit: false,
                date: '',
                time: '',
                menu: false,
                modal: false,
                menu2: false,
                snack: false,
                snackColor: '',
                snackText: '',
                loading: true,
                loadingCards: true,
                loadingAviableCards: true,
                snackbar: false,
                dialog: false,
                radioGroup: 1,
                deleteDialog: false,
                search: '',
                text: 'Oops... Something went wrong',
                timeout: 5000,
                newBalance: '',
                regions: [],
                typeCars: [],
                typeTransport: [],
                details: {
                    name_client: "",
                    surname_client: "",
                    phone: "",
                    date: '',
                    time: '',
                    address_from: "",
                    address_to: "",
                    floor_from: '',
                    floor_to: '',
                    city_from: '',
                    city_to: '',
                    text : "",
                    first_lift:false,
                    second_lift: false,
                    first_entryway: false,
                    second_entryway: false,
                    first_crane: false,
                    second_crane: false,
                    transportation_cost: '',
                    lead_cost: '',
                    category: false,
                    status: false,
                    region: null,
                    comment: '',
                    type_car: '',
                    type_transport: '',
                    hot: ''
                },
                mask: '###-###-####',
                rules: {
                    counter: value => (value.toString().length <= 10) || this.$translate.locale['Max'] + ' 10',
                    comment: value => (value.length <= 500) || this.$translate.locale['Max'] + ' ' + 500 + ' ' + this.$translate.locale['characters'],
                    intNumber: value => {
                        const pattern = /^(\d+|$)$/;
                        return pattern.test(value) || this.$translate.locale['Invalid number.']
                    },
                    number: value => {
                        const pattern = /^(?=.+)(?:[1-9]\d*|0)?(?:\.\d+)?$/;
                        return pattern.test(value) || this.$translate.locale['Invalid number.']
                    },
                    numberReverse: value => {
                        const pattern = /^-\d+$/;
                        return (pattern.test(value) || value <= 0) || this.$translate.locale['Invalid number.']
                    },
                    phone: value => value.length <= 10 || this.$translate.locale['Min 10 characters'],
                    required: value => (!!value || value === 0) || this.$translate.locale['Required.'],
                    email: value => {
                        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                        return (pattern.test(value) || !value) || this.$translate.locale['Invalid e-mail.']
                    },
                },
            }
        },
        methods: {
            createLead() {
                if (!this.$refs.form.validate()) {
                    this.text = "Fill the form correctly";
                    this.snackbar = true;
                } else {
                    this.loading = true;
                    axios.post(`${this.$hostname}/api/createLead/`, {...this.details})
                        .then((response) => {
                            if (response.status === 201) {
                                this.text = "Lead created";
                                this.snackbar = true;
                                this.dialog = false;
                                this.loading = false;
                                console.log(response.data)
                                setTimeout(() => {
                                    this.$router.push(`/leads/${response.data.id}/details`)
                                }, 500)
                            }
                        }).catch((error) => {
                            this.text = "Connection error";
                            console.log(error)
                            this.snackbar = true;
                            this.dialog = false;
                    })
                }
            }
        },
        beforeCreate() {
            if (!this.$session.exists()) {
                this.$router.push('/')
            }
        },
        mounted() {
            axios.get(`${this.$hostname}/api/regions/`)
                .then((response) => {
                    if (response.status === 200) {
                        this.regions = response.data;
                        console.log(this.regions)
                    }
                }).catch((error) => {
                this.text = "Connection error";
                console.log(error)
                this.snackbar = true;
                this.dialog = false;
            });
            axios.get(`${this.$hostname}/api/cars/`)
                .then((response) => {
                    if (response.status === 200) {
                        this.typeCars = response.data;
                        console.log(this.typeCars)
                    }
                }).catch((error) => {
                this.text = "Connection error";
                console.log(error)
                this.snackbar = true;
                this.dialog = false;
            });
            axios.get(`${this.$hostname}/api/transportationTypes/`)
                .then((response) => {
                    if (response.status === 200) {
                        this.typeTransport = response.data;
                        console.log(this.typeTransport)
                    }
                }).catch((error) => {
                this.text = "Connection error";
                console.log(error)
                this.snackbar = true;
                this.dialog = false;
            })

        }
    }
</script>

<style scoped>
    .v-list__tile__content ~ .v-list__tile__avatar {
        justify-content: flex-start;
    }

    .v-list__tile__content {
        flex: initial;
    }

    .v-input--selection-controls {
        /*margin-top: 22px;*/
        /*margin-left: 14px;*/
    }
</style>
