import axios from "axios";
import { jwt } from "./jwt";
import store from '@/vuex'
import router from '@/router'

export const client = axios.create({
  baseURL: process.env.VUE_APP_BASE_URL,
});

client.interceptors.request.use((request) => {
  const token = jwt.getToken();
  if (token) {
    request.headers.common["Authorization"] = "Bearer " + token;
  }
  return request;
});

client.interceptors.response.use(
  (response) => {
    return response;
  },
  function(error) {
    if (error.response.status === 401) {
      store.dispatch("signOut");
      router.replace("/login");
    }
    return Promise.reject(error);
  }
);

const auth = {
  createToken({ username, password }) {
    return client.post("token/obtain/", { username, password });
  },
  createUser(payload) {
    return client.post("users/", payload);
  },
};

const users = {
  current() {
    return client.get("users/current/");
  },
  resetPassword(payload) {
    return client.post("users/reset_password/", payload);
  },
  resetPasswordConfirm(payload) {
    return client.post("users/reset_password_confirm/", payload);
  },
};
const courses = {
  getCourses(payload) {
    return client.get("courses/", {
      params: {
        limit: payload["limit"],
        offset: payload["offset"],
        category: payload["category"],
      },
    });
  },
  getCategories() {
    return client.get("categories/");
  },
  getCourse(id) {
    return client.get(`courses/${id}/`);
  },
  joinCourse(id) {
    return client.post(`courses/${id}/enroll_as_student/`);
  },
};

export const http = {
  auth,
  users,
  courses,
};
