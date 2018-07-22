import Vue from 'vue';
import Vuex from 'vuex';
import persistedState from 'vuex-persistedstate';

import modules from './modules';

Vue.use(Vuex);

export default new Vuex.Store({
  modules,
  plugins: [persistedState()],
  strict: process.env.NODE_ENV !== 'production',
});
