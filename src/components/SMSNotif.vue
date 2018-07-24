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
          <input
            type="text"
            v-model="phoneNum"
            :class="{animated: error, shake: error}"
            class="smsnotif"
          >
        </div>
    </div>
  </div>
  <div class='mainItem3'>
    <button class="back-button" @click="$router.push({ name: 'service' })">BACK</button>
    <button class="large inqueue-buttons" @click="setPhone">CONTINUE</button>
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
    error: false,
  }),
  methods: {
    setPhone() {
      if (this.phoneNum.length > 0) {
        this.SET_PHONE(this.phoneNum);
        this.$router.push({ name: 'inqueue' });
      } else {
        this.error = true;
      }
    },
    ...mapMutations([
      'SET_PHONE',
    ]),
  },
};
</script>

