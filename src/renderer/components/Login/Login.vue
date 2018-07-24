<template>
  <div class="qr-reader-container">
    <div class="logo-container">
      <img src="../../assets/img/logo.png" style="height: 100%;"/>
    </div>
    <div class="qr-title">Please Scan your Teller QR Code.</div>
    <div class="qr-reader-box">
      <qrcode-reader @init="onInit" @decode="onDecode" :paused="paused"></qrcode-reader>
    </div>
  </div>
</template>

<script>
import 'vue-qrcode-reader/dist/vue-qrcode-reader.css';
import { QrcodeReader } from 'vue-qrcode-reader/dist/vue-qrcode-reader.common';
import { mapMutations, mapState } from 'vuex';

export default {
  data() {
    return {
      paused: false,
      want: null,
      flag: null,
    };
  },
  computed: {
    ...mapState('User', [
      'uuid',
    ]),
  },
  methods: {
    async onInit(promise) {
      // show loading indicator
      try {
        await promise;
        // successfully initialized
      } catch (error) {
        if (error.name === 'NotAllowedError') {
          // user denied camera access permisson
        } else if (error.name === 'NotFoundError') {
          // no suitable camera device installed
        } else if (error.name === 'NotSupportedError') {
          // page is not served over HTTPS (or localhost)
        } else if (error.name === 'NotReadableError') {
          // maybe camera is already in use
        } else if (error.name === 'OverconstrainedError') {
          // passed constraints don't match any camera.
          // Did you requested the front camera although there is none?
        } else {
          // browser is probably lacking features (WebRTC, Canvas)
        }
      } finally {
        // hide loading indicator
      }
    },
    onDecode(content) {
      // Start of run only when successful login.
      this.paused = true;
      this.flag = content;
      if (this.flag !== '') {
        this.SET_UUID(content);
        this.want = this.uuid;
        this.$router.push({
          path: '/priority/',
        });
      } else {
        this.paused = false;
      }
      // End of run only when successful login.
    },
    ...mapMutations('User', [
      'SET_UUID',
    ]),
  },
  components: {
    QrcodeReader,
  },
};
</script>

<style lang="scss" scoped>
@import "../../assets/sass/styles.scss";
</style>
