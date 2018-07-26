<template>
  <div class='service-screen-container'>
    <div class="screen-card"
      v-for="service in services"
      :key="service.pk"
      v-if="hasActive(service.teller)"
    >
      <div class='service-screen'>
        <p class="titleStyle">{{ service.service_name }}</p>
      </div>
      <div class="teller-screen" v-for="teller in service.teller" :key="teller.key">
        <div class="full-width" v-if="teller.is_active">
          <div class="label-row">
            <p class="label-item">Teller #</p>
            <p class="label-item">Number Served</p>
          </div>
          <div class="data-row" style="margin: 20px 0px;">
            <p class="data-item"> {{ teller.pk}} </p>
            <p class="data-item">{{ teller.current }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "../assets/sass/styles.scss";
</style>

<script>
/* eslint-disable */
import axios from 'axios';
import moment from 'moment';

export default {
  data: () => ({
    services: [],
    chatSocket: null,
    authToken: 'pk 1',
    data: null,
  }),
  methods: {
    hasActive(teller) {
      let ret = teller.find(obj => {
        return obj.is_active === true;
      });

      return (ret === undefined) ? false: true;
    },
    parseDate(date) {
      let ret = '-';
      if (date.length > 0) {
        ret = moment(date).fromNow(true);
      }

      return ret;
    },
  },
  mounted() {
    axios.get('http://192.168.254.135:8000/transaction/1/getscreen', {
    }).then((response) => {
      this.services = response.data.service;
      this.chatSocket = new WebSocket(`ws://192.168.254.135:8000/ws/customer/1/2/?pk=${this.authToken}`);
      this.chatSocket.onmessage = (e) => {
        let ind = null;
        let ind_1 = null;
        this.data = JSON.parse(e.data);
        if(this.data.message === 'current served change') {
          const service_pk = this.data.service_pk;
          const teller_pk = this.data.teller_pk;
          // eslint-disable-next-line
          ind = this.services.findIndex(function (service) {
            return String(service.pk) === String(service_pk);
          });
          // eslint-disable-next-line
          ind_1 = this.services[ind].teller.findIndex(function (tel) {
            return String(tel.pk) === String(teller_pk);
          });
          this.services[ind].teller[ind_1].current = this.data.current_served;
        } else if(this.data.message === 'teller online change') {
          const service_pk = this.data.service_pk;
          const teller_pk = this.data.teller_pk;
          // eslint-disable-next-line
          ind = this.services.findIndex(function (service) {
            return String(service.pk) === String(service_pk);
          });
          // eslint-disable-next-line
          ind_1 = this.services[ind].teller.findIndex(function (tel) {
            return String(tel.pk) === String(teller_pk);
          });
          this.services[ind].teller[ind_1].is_active = (this.data.is_active === 'true');
        }
      };
    });
  },
};
</script>

