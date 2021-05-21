import Vue from "vue";
import Vuex from "vuex";
import { jwt } from "./services/jwt";
import { http } from "./services/http";

Vue.use(Vuex);

const state = {
  user: null,
  isAutenticated: null,
  courses: [],
  countOfCourses: null,
  categories: [],
  course: null,
};

const store = new Vuex.Store({
  state,
  getters: {
    user: (state) => {
      return state.user;
    },
    isAutenticated: (state) => {
      return state.isAutenticated;
    },
    courses: (state) => {
      return state.courses;
    },
    countOfCourses: (state) => {
      return state.countOfCourses;
    },
    categories: (state) => {
      return state.categories;
    },
    course: (state) => {
      return state.course;
    },
  },

  actions: {
    signIn({ commit, dispatch }, payload) {
      return http.auth.createToken(payload).then((response) => {
        commit("setAuth", response.data.token);
        return dispatch("getCurrentUser");
      });
    },
    signUp({ commit }, payload) {
      return http.auth.createUser(payload).then((response) => {
        commit("setAuth", response.data.token);
        commit("setUser", response.data.user);
      });
    },
    signOut({ commit }) {
      commit("purgeAuth");
    },
    getCurrentUser({ commit }) {
      return http.users
        .current()
        .then((response) => commit("setUser", response.data));
    },
    resetPassword(_, payload) {
      return http.users.resetPassword(payload);
    },
    resetPasswordConfirm(_, payload) {
      return http.users.resetPasswordConfirm(payload);
    },
    getCourses({ commit }, payload) {
      return http.courses.getCourses(payload).then((response) => {
        commit("setCourses", response.data.results);
        commit("setCountOfCourses", response.data.count);
      });
    },
    getCategories({ commit }) {
      return http.courses
        .getCategories()
        .then((response) => commit("setCategories", response.data));
    },
    getCourse({ commit }, payload) {
      return http.courses
        .getCourse(payload)
        .then((response) => commit("setCourse", response.data));
    },
    joinCourse(_, payload) {
      return http.courses.joinCourse(payload);
    },
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setAuth(state, token) {
      state.isAutenticated = true;
      jwt.setToken(token);
    },
    purgeAuth(state) {
      state.user = null;
      state.isAutenticated = false;
      jwt.removeToken();
    },
    setCourses(state, courses) {
      state.courses = courses;
    },
    setCountOfCourses(state, count) {
      state.countOfCourses = count;
    },
    setCategories(state, categories) {
      state.categories = categories;
    },
    setCourse(state, course) {
      state.course = course;
    },
  },
});

export default store;
