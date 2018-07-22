<template>
  <div>Logging out</div>
</template>

<script>
import { mapMutations } from 'vuex';
import axios from 'axios';

export default {
  data: () => ({
    uuid: '889d5bb11b79450e89aaca1c210744e7',
  }),
  methods: {
    ...mapMutations('User', [
      'DELETE_UUID',
    ]),
  },
  mounted() {
    axios.post('http://192.168.1.5:8000/teller/logout/', {
      uuid: this.uuid,
    });
    this.DELETE_UUID();
    this.$router.push({ name: 'login' });
  },
};
</script>
