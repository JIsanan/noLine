<template>
  <div class='parent'>
      <div class='child ' id='box-shadow'>
        <div v-if='prioNum' >
          <div class='textStyle'>Now Serving</div>
          <div class='prio-container'>
              <p class='prioNumStyle'>{{ prioNum }}</p>
          </div>
          <div class='textStyle'>People in Line</div>
          <div class='prio-container'>
              <p class='prioNumStyle'>{{ inline }}</p>
          </div>
          <div class='inputparent'>
              <button class='buttonComplete large' @click="onComplete">COMPLETE</button>
              <button class='buttonSkip large' @click="onSkip">CANCEL</button>
              <button class='buttonSkip large' @click="onLogout">LOGOUT</button>
          </div>
        </div>
        <div v-else>
          <div class='textStyle'> No one is currently lining up.</div>
        </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default{
  data: () => ({
    data: null,
    inline: null,
    prioNum: null,
    service_type: null,
    service_id: 6,
    service_name: null,
    authToken: 'uuid 889d5bb11b79450e89aaca1c210744e7',
    uuid: '889d5bb11b79450e89aaca1c210744e7',
    chatSocket: null,
  }),
  mounted() {
    this.uuid = this.GET_UUID();
    axios.post(`${process.env.API_URL}/teller/authenticate/`, {
      uuid: this.uuid,
    }).then((response) => {
      if (response.data.message === 'successfully connected') {
        this.inline = this.data.amount_of_people;
        this.service_name = response.data.service_name;
        this.chatSocket = new WebSocket(`${process.env.WS_URL}/teller/${this.service_id}/?uuid=${this.authToken}`);
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
        this.chatSocket = new WebSocket(`${process.env.WS_URL}/teller/${this.service_id}/?uuid=${this.authToken}`);
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
      axios.post(`${process.env.API_URL}/teller/finish/`, {
        uuid: this.uuid,
      });
    },
    onSkip() {
      axios.post(`${process.env.API_URL}/teller/skip/`, {
        uuid: this.uuid,
      });
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
