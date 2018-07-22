<template>
  <div>Logging out</div>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
  methods: {
    ...mapMutations('User', [
      'DELETE_UUID',
    ]),
  },
  mounted() {
    this.DELETE_UUID();
    this.$router.push({ name: 'login' });
  },
};
</script>
