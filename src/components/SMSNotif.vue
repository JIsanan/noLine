<template>
 <div class='inqueue-container'>
    <div class='sms-card-container top-bottom'>
        <p class='smsStyle'>
          SMS Notification
        </p>
    </div>
  <div class="sms-card-container">
    <div class='mainItem1'>
        <div class='ETAstyle'>
          <p class='label-text'>Please input your phone number below.</p>
          <div class='input-forms'>
            <p class="sms-prefix">+63</p>
            <input
              type="text"
              v-model="phoneNum"
              :class="{animated: error, shake: error}"
              class="smsnotif"
            >
          </div>
        </div>
    </div>
    <div class='mainItem2'>
          <span class='label-text'>Notify when only </span>
            <input
              type="text"
              v-model="peopleNum"
              :class="{animated: error, shake: error}"
              class="notifnum"
            >
          <p class='label-text'>people are ahead of me.</p>
    </div>
  </div>
  <div class='mainItem3'>
    <button class="back-button gray" @click="$router.push({ name: 'checkqueue' })">BACK</button>
    <button class="large inqueue-buttons green" @click="setPhone">CONTINUE</button>
    <button
      class="large inqueue-buttons blue"
      @click="$router.push({ name: 'inqueue' })"
    >
      SKIP
    </button>
  </div>
</div>
</template>

<style lang="scss" scoped>
  @import "../assets/sass/styles.scss";
  @import "../assets/sass/icons.scss";
</style>

<script>
import { mapMutations } from 'vuex';

export default {
  data: () => ({
    phoneNum: '',
    peopleNum: '3',
    error: false,
  }),
  methods: {
    setPhone() {
      if (this.phoneNum.length > 0 &&
        (isNaN(Number(this.peopleNum)) &&
        Number(this.peopleNum) > 0)) {
        this.SET_PHONE(this.phoneNum);
        this.SET_PEOPLE_LEFT(Number(this.peopleNum));
        this.$router.push({ name: 'inqueue' });
      } else {
        this.error = true;
      }
    },
    ...mapMutations([
      'SET_PHONE',
      'SET_PEOPLE_LEFT',
    ]),
  },
};
</script>

