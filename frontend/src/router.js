import Vue from "vue";
import Router from "vue-router";
import Register from "./components/Register.vue";
import Login from "./components/Login.vue";
import Home from "./components/Home.vue";
import Forgot from "./components/Forgot.vue";
import Reset from "./components/Reset.vue";
import Courses from "./components/Courses.vue";
import Course from "./components/Course.vue";
import { jwt } from "./services/jwt";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    { path: "/", component: Home },
    {
      path: "/login",
      name: "login",
      component: Login,
      beforeEnter: (to, from, next) => {
        if (!jwt.getToken()) next();
        else next(false);
      },
    },
    {
      path: "/register",
      component: Register,
      beforeEnter: (to, from, next) => {
        if (!jwt.getToken()) next();
        else next(false);
      },
    },
    {
      path: "/forgot",
      component: Forgot,
      beforeEnter: (to, from, next) => {
        if (!jwt.getToken()) next();
        else next(false);
      },
    },
    {
      path: "/reset/:uid/:token",
      component: Reset,
      beforeEnter: (to, from, next) => {
        if (!jwt.getToken()) next();
        else next(false);
      },
    },
    {
      path: "/courses",
      component: Courses,
    },
    {
      path: "/course/:id/promo",
      component: Course,
      props: true,
    },
  ],
});
