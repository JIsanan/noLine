const state = {
  uuid: '',
};

const mutations = {
  SET_UUID(state, uuid) {
    state.uuid = uuid;
  },
  DELETE_UUID(state) {
    state.uuid = '';
  },
};

const getters = {
  IS_LOGGED_IN(state) {
    return state.uuid.length > 0;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
};
