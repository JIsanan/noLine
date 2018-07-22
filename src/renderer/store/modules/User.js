const state = {
  uuid: -1, // uuid is -1 if there is no active login.
};

const mutations = {
  SET_UUID(state, uuid) {
    state.uuid = uuid;
  },
  DELETE_UUID(state) {
    state.uuid = -1;
  },
};

const getters = {
  IS_LOGGED_IN(state) {
    return state.uuid > 0;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
};
