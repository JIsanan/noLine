<template>
  <div class='service-container'>
    <div class="instruction-row">
      <p>Hello, click on a service.</p>
    </div>
    <button class='service'
      v-for="service in services"
      :key="service.pk"
      :disabled="service.online_tellers == 0"
      @click="setService(service.service_name, service.pk)"
    >
      <p class="titleStyle">{{ service.service_name }}</p>
      <div class="label-row">
        <p class="label-item">Current Customers in line</p>
        <p class="label-item">Waiting Time</p>
        <p class="label-item"># of Online Tellers</p>
      </div>
      <div class="data-row">
        <p class="data-item"> {{ service.people_in_line }} </p>
        <p class="data-item">{{ parseDate(service.eta) }}</p>
        <p class="data-item">{{ service.online_tellers }}</p>
      </div>
    </button>
  </div>
</template>

<style lang="scss" scoped>
@import "../assets/sass/styles.scss";
</style>

<script>
import axios from 'axios';
import moment from 'moment';
import { mapState, mapMutations } from 'vuex';

export default{
  data: () => ({
    services: [],
    chatSocket: null,
    authToken: 'pk 1',
    data: null,
    ind: null, // index of the service whose # of people in line changes
  }),
  methods: {
    parseDate(date) {
      let ret = '-';
      if (date.length > 0) {
        ret = moment(date).fromNow(true);
      }

      return ret;
    },
    setService(name, pk) {
      this.$store.dispatch('SET_SERVICE', {
        name,
        pk,
      });
      this.$router.push({ name: 'checkqueue' });
    },
    ...mapMutations([
      'SET_PK',
    ]),
  },
  computed: {
    ...mapState([
      'pk',
    ]),
  },
  mounted() {
    axios.get('http://192.168.254.135:8000/transaction/1/getservice/', {
    }).then((response) => {
      this.services = response.data.service;
      this.chatSocket = new WebSocket(`ws://192.168.254.135:8000/ws/customer/1/1/?pk=${this.authToken}`);
      this.chatSocket.onmessage = (e) => {
        this.data = JSON.parse(e.data);
        if (this.data.message === 'line change') {
          const data = this.data.service_pk;
          // eslint-disable-next-line
          this.ind = this.services.findIndex(function (service) {
            return String(service.pk) === String(data);
          });
          this.services[this.ind].people_in_line = this.data.number_of_people;
          this.services[this.ind].eta = this.data.eta;
        } else if (this.data.message === 'teller change') {
          const data = this.data.service_pk;
          // eslint-disable-next-line
          this.ind = this.services.findIndex(function (service) {
            return String(service.pk) === String(data);
          });
          this.services[this.ind].online_tellers = this.data.number_of_people;
        }
      };
    });
  },
};
</script>
