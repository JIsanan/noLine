<template>
  <div class='service-container'>
    <div class="instruction-row">
      <p>Hello, click on a service.</p>
    </div>
    <div class='service' v-for="service in services" :key="service.id">
      <p class="titleStyle">{{ service.service_name }}</p>
      <div class="label-row">
        <p class="label-item">Current Customers in line</p>
        <p class="label-item"># of Online Tellers</p>
      </div>
      <div class="data-row">
        <p class="data-item"> {{ service.people_in_line }} </p>
        <p class="data-item">{{ service.online_tellers }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default{
  data: () => ({
    service_name: null,
    services: [],
    chatSocket: null,
    authToken: 'pk 1',
    data: null,
    ind: null,
  }),
  mounted() {
    axios.get('http://192.168.1.5:8000/transaction/1/getservice', {
    }).then((response) => {
      this.services = response.data.service;
      this.chatSocket = new WebSocket(`ws://192.168.1.5:8000/ws/customer/6/1/?pk=${this.authToken}`);
      this.chatSocket.onmessage = (e) => {
        this.data = JSON.parse(e.data);
        if (this.data.message === 'line change') {
          const data = this.data.service_pk;
          // eslint-disable-next-line
          this.ind = this.services.findIndex(function (service) {
            return String(service.pk) === String(data);
          });
          this.services[this.ind].people_in_line = this.data.number_of_people;
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
<style lang="scss" scoped>
@import "../assets/sass/styles.scss";
</style>
