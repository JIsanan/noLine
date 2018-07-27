<template>
  <div>Logging out</div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
import axios from 'axios';

export default {
  data: () => ({
    uuid: null,
  }),
  methods: {
    ...mapMutations('User', [
      'DELETE_UUID',
    ]),
  },
  computed: {
    ...mapGetters('User', [
        'GET_UUID',
      ]),
  },
  mounted() {
    this.uuid = this.GET_UUID();
    axios.post('http://192.168.43.135:8000/teller/logout/', {
      uuid: this.uuid,
    });
    this.DELETE_UUID();
    this.$router.push({ name: 'login' });
  },
};
</script>
