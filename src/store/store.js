import Vue from 'vue';
import Vuex from 'vuex';
import persistedState from 'vuex-persistedstate';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    pk: -1,
    phoneNum: '',
    serviceName: '',
    lineLater: '',
    peopleLeft: -1,
  },
  mutations: {
    SET_PK: (state, pk) => {
      state.pk = pk;
    },
    SET_SERVICE_NAME: (state, name) => {
      state.serviceName = name;
    },
    SET_PHONE: (state, phoneNum) => {
      state.phoneNum = `63${phoneNum}`;
    },
    SET_PEOPLE_LEFT: (state, peopleLeft) => {
      state.peopleLeft = peopleLeft;
    },
    SET_LINE_STATUS: (state, lineFlag) => {
      state.lineLater = lineFlag;
    },
    REMOVE_ALL: (state) => {
      state.pk = -1;
      state.phoneNum = '';
      state.serviceName = '';
      state.lineLater = '';
    },
  },
  actions: {
    SET_SERVICE({ commit }, service) {
      commit('SET_PK', service.pk);
      commit('SET_SERVICE_NAME', service.name);
    },
  },
  plugins: [persistedState()],
});
