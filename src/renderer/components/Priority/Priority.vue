<template>
  <div class='parent'>
      <div class='child'>
        <div class="service-box">
          <div class="company-container">
            <div class='company-text'>{{ company_name }}</div>
            <div class='company-service'>{{ service_name }}</div>
          </div>
          <div class="company-container">
            <div class='company-service'># of Customers waiting</div>
            <div class='company-text strong'>{{ inline }}</div>
          </div>
          <button class='' @click="onLogout">LOGOUT</button>
        </div>
        <div v-if='prioNum' >
          <div class='textStyle'>Now Serving</div>
          <div class='prio-container'>
              <p class='prioNumStyle'>{{ prioNum }}</p>
          </div>
          <div class='inputparent'>
              <button class='buttonSkip large' @click="onSkip">CANCEL</button>
              <button class='buttonComplete large' @click="onComplete">COMPLETE</button>
          </div>
        </div>
        <div v-else>
          <div class='inputparent' style="margin: 60px 0px;">
            <mikepad :size="size"></mikepad>
          </div>
          <div class='textStyle' style="margin:60px 0px;"> No one is currently lining up.</div>
        </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import Mikepad from 'vue-loading-spinner/src/components/Mikepad';

export default{
  components: {
    Mikepad,
  },
  data: () => ({
    API_URL: 'http://192.168.43.135:8000',
    WS_URL: 'ws://192.168.43.135:8000/ws',
    data: null,
    test: null,
    inline: null,
    prioNum: null,
    service_type: null,
    service_id: null,
    service_name: null,
    authToken: null,
    company_name: null,
    uuid: null,
    chatSocket: null,
    bool: true,
    size: '80px',
  }),
  mounted() {
    this.uuid = this.GET_UUID();
    this.authToken = `uuid ${this.uuid}`;
    axios.post(`${this.API_URL}/teller/authenticate/`, {
      uuid: this.uuid,
    }).then((response) => {
      if (response.data.message === 'successfully connected') {
        this.prioNum = response.data.priority_num;
        this.inline = response.data.amount_of_people;
        this.service_name = response.data.service_name;
        this.service_id = response.data.service_pk;
        this.company_name = response.data.company_name;
        this.chatSocket = new WebSocket(`${this.WS_URL}/teller/${this.service_id}/?uuid=${this.authToken}`);
        this.chatSocket.onmessage = (e) => {
          this.data = JSON.parse(e.data);
          if (this.data.message === 'get new customer') {
            this.prioNum = this.data.priority_num;
          } else if (this.data.message === 'change of amount') {
            this.inline = this.data.amount_of_people;
          } else {
            this.service_type = this.data;
          }
        };
      } else if (response.data.message === 'continue') {
        this.prioNum = response.data.priority_num;
        this.inline = response.data.amount_of_people;
        this.service_id = response.data.service_pk;
        this.service_name = response.data.service_name;
        this.company_name = response.data.company_name;
        this.chatSocket = new WebSocket(`${this.WS_URL}/teller/${this.service_id}/?uuid=${this.authToken}`);
        this.chatSocket.onmessage = (e) => {
          this.data = JSON.parse(e.data);
          if (this.data.message === 'get new customer') {
            this.prioNum = this.data.priority_num;
          } else if (this.data.message === 'change of amount') {
            this.inline = this.data.amount_of_people;
          } else {
            this.service_type = this.data;
          }
        };
      } else if (response.data.message === 'incorrect') {
        this.$router.push({ name: 'logout' });
      }
    });
  },
  methods: {
    ...mapGetters('User', [
      'GET_UUID',
    ]),
    onComplete() {
      axios.post(`${this.API_URL}/teller/finish/`, {
        uuid: this.uuid,
      });
      this.prioNum = null;
    },
    onSkip() {
      axios.post(`${this.API_URL}/teller/skip/`, {
        uuid: this.uuid,
      });
      this.prioNum = null;
    },
    onLogout() {
      this.$router.push({ name: 'logout' });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../../assets/sass/styles.scss";
</style>
