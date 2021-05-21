<template>
  <div id="form">
    <b-form @submit.prevent="onSubmit">
      <b-form-group
        id="input-group-1"
        label="Your Username:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.username"
          placeholder="Username"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-2"
        label="Your Password:"
        label-for="input-2"
      >
        <b-form-input
          id="input-5"
          v-model="form.password"
          type="password"
          placeholder="Password"
          required
        ></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Login</b-button>
      <br />
      <router-link to="/forgot">Remind the password</router-link>
    </b-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    onSubmit() {
      this.$store
        .dispatch("signIn", {
          username: this.form.username,
          password: this.form.password,
        })
        .then(() => this.$router.push(this.$route.query.redirect || "/"))
        .catch(() =>
          this.$bvToast.toast(`No found active user with credential fields`, {
            title: "Error",
            variant: "danger",
            solid: true,
            autoHideDelay: 5000,
          })
        );
    },
  },
};
</script>
<style scoped>
#form {
  width: 400px;
  margin: auto;
  margin-top: 30px;
}
</style>