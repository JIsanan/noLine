<template>
  <div>
    qrcode login:
    <qrcode-reader @init="onInit" @decode="onDecode" :paused="paused"></qrcode-reader>

    For testing only: <router-link to="/priority/">Show me the priority view</router-link>
  </div>
</template>

<script>
import 'vue-qrcode-reader/dist/vue-qrcode-reader.css';
import { QrcodeReader } from 'vue-qrcode-reader/dist/vue-qrcode-reader.common';

export default {
  data() {
    return {
      paused: false,
    };
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
      // Toggle flag only on successful login
      console.log(content);
      this.paused = true;
    },
  },
  components: {
    QrcodeReader,
  },
};
</script>
