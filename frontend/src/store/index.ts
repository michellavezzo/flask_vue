import { createStore } from "vuex";
import userModule from "./user";

const store = createStore({
    modules: {
        user: userModule,
    },
    state: {
        timezoneSelected: "",
    },
    mutations: {
        SET_TIMEZONE(state, timezone) {
            state.timezoneSelected = timezone;
        },
    },
    actions: {
        setTimezone({ commit }, timezone) {
            commit("SET_TIMEZONE", timezone);
        },
    },
    getters: {
        timezoneSelected: (state) => state.timezoneSelected,
    },
});

export default store;
