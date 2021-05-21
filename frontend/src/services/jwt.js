export const jwt = {
  getToken() {
    return localStorage.getItem("token");
  },
  removeToken() {
    localStorage.removeItem("token");
  },
  setToken(token) {
    localStorage.setItem("token", token);
  },
};
