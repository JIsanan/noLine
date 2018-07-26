<template>
 <div class='inqueue-container'>
  <div class="inqueue-card-container">
    <div class='mainItem4'>
        <p class='serviceStyle'>
          {{ serviceTitle }}
        </p>
    </div>
    <div class='mainItem1'>
        <div class='ETAstyle'>
          <span class='label-text' v-if="lineLater === 'true'">If you line now:</span>
          <p class='label-text'>Estimated Service Time</p>
          <p class='data-text'>{{ parseDate() }}</p>
          <p class='label-text'>Priority Num #:</p>
          <p class='data-text last-child'>{{ priorityNum}}</p>
        </div>
        <div class='QRstyle'>
          <img class="img-qr" :src="qrURL">
        </div>
    </div>
  </div>
  <div class='mainItem3'>
      <button
        class="large inqueue-buttons blue right"
        @click="$router.push({ name: 'root' })"
      >
        Finish
      </button>
  </div>
</div>
</template>

<style lang="scss" scoped>
  @import "../assets/sass/styles.scss";
</style>

<script>
import axios from 'axios';
import { mapState, mapMutations } from 'vuex';
import moment from 'moment';

export default {
  data: () => ({
    serviceTitle: '',
    serviceTime: '',
    priorityNum: '',
    qrURL: '',
  }),
  methods: {
    parseDate() {
      return moment(this.serviceTime).format('hh:mm A');
    },
    ...mapMutations([
      'REMOVE_ALL',
    ]),
  },
  computed: {
    ...mapState([
      'pk',
      'phoneNum',
      'serviceName',
      'lineLater',
      'peopleLeft',
    ]),
  },
  mounted() {
    this.serviceTitle = this.serviceName;
    axios.post(`http://192.168.254.135:8000/transaction/${this.pk}/joinqueue/`, {
      when_to_notify: this.peopleLeft,
      phone_num: this.phoneNum,
      linelater: this.lineLater,
    }).then((response) => {
      this.serviceTime = response.data.waiting_time;
      this.priorityNum = response.data.priority_number;
      this.qrURL = `https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=${response.data.uuid}`;
      this.REMOVE_ALL();
    });
  },
};
</script>

