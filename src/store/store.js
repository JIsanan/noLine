import Vue from 'vue';
import Vuex from 'vuex';
import persistedState from 'vuex-persistedstate';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    pk: -1,
    phoneNum: '',
  },
  mutations: {
    SET_PK: (state, pk) => {
      state.pk = pk;
    },
    SET_PHONE: (state, phoneNum) => {
      state.phoneNum = phoneNum;
    },
    REMOVE_ALL: (state) => {
      state.pk = -1;
      state.phoneNum = '';
    },
  },
  plugins: [persistedState()],
});
