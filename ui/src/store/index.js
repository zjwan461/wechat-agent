import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    sysInfo: {
    }
  },
  mutations: {
    setSysInfo(state, sysInfo) {
      state.sysInfo = sysInfo
    }
  },
  actions: {
  },
  modules: {
  }
})
