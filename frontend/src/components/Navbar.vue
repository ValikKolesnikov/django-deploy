<template>
  <b-navbar toggleable="lg" type="dark" variant="primary">
    <router-link tag="b-navbar-brand" to="/">E-Learning App</router-link>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="ml-auto">
        <router-link tag="b-nav-item" to="/courses">Courses</router-link>
      </b-navbar-nav>
      <b-navbar-nav v-if="!user" class="ml-auto">
        <router-link tag="b-nav-item" to="/login">Login</router-link>
        <router-link tag="b-nav-item" to="/register">Register</router-link>
      </b-navbar-nav>
      <b-navbar-nav v-if="user" class="ml-auto">
        <b-nav-item href="#" @click="onLogout">Logout</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "Navbar",
  methods: {
    onLogout() {
      this.$store.dispatch("signOut");
      this.$router.push("/login");
    },
  },
  computed: {
    ...mapGetters(["user"]),
  },
};
</script>