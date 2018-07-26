<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
// import axios from 'axios';
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'App',
  data: () => ({
    services: [],
    chatSocket: null,
    authToken: 'pk 1',
    data: null,
    ind: null,
  }),
  computed: {
    ...mapState([
      'pk',
    ]),
  },
  methods: {
    ...mapMutations([
      'SET_PK',
    ]),
  },
  mounted() {
    this.chatSocket = new WebSocket(`ws://192.168.254.135:8000/ws/customer/1/1/?pk=${this.authToken}`);
    this.chatSocket.onmessage = (e) => {
      this.data = JSON.parse(e.data);
      if (this.data.message === 'teller change' && this.$route.name !== 'screen') {
        // eslint-disable-next-line
        if (parseInt(this.data.service_pk) === parseInt(this.pk) && parseInt(this.data.number_of_people) === 0) {
          this.SET_PK(-1);
          this.$router.push({ name: 'service' });
        }
      }
    };
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
