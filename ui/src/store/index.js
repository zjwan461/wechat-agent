import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    serverInfo: {
    }
  },
  mutations: {
    setServerInfo(state, serverInfo) {
      state.serverInfo = serverInfo
    }
  },
  actions: {
  },
  modules: {
  }
})
