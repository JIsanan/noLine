<template>
<div class="checkqueue-container">
  <div class='pickprocess-container'>
        <button class="tab-buttons now" type="button" @click="setLineStatus('false')">
          <div class="tab-header">Start Lining Up</div>
          <div class="tab-body">You will be placed at the last in line.</div>
        </button>
        <button class="tab-buttons later" type="button" @click="setLineStatus('true')">
          <div class="tab-header">Decide Later</div>
          <div class="tab-body">You may decide when to line up using our application.</div>
        </button>
        <div></div>
  </div>
  <div style="display:flex;justify-content:center;">
    <button
          class="large inqueue-buttons gray back-button"
          @click="$router.push({ name: 'root' })"
        >
          BACK
        </button>
  </div>
</div>
</template>

<style lang="scss" scoped>
  @import "../assets/sass/styles.scss";
</style>

<script>
import { mapMutations } from 'vuex';

export default {
  methods: {
    setLineStatus(flag) {
      this.SET_LINE_STATUS(flag);
      this.$router.push({ name: 'smsnotif' });
    },
    ...mapMutations([
      'SET_LINE_STATUS',
    ]),
  },
};
</script>

