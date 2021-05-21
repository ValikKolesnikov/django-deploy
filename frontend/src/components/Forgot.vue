<template>
  <div id="form">
    <h3>Forgot your password?</h3>
    <p>
      Enter your e-mail address and we will send you an email with a link to
      reset your password.
    </p>
    <b-form @submit.prevent="onSubmit">
      <b-form-group id="input-group-2" label="Your Email:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="email"
          type="email"
          placeholder="Enter email"
          required
        ></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Reset the password</b-button>
    </b-form>
  </div>
</template>
<script>
export default {
  name: "Forgot",
  data() {
    return {
      email: "",
    };
  },
  methods: {
    onSubmit() {
      this.$store
        .dispatch("resetPassword", { email: this.email })
        .then(() =>
          this.$bvToast.toast(`The letter was sent on your email`, {
            title: "E-learning App",
            variant: "info",
            solid: true,
            autoHideDelay: 5000,
          }),
          () =>
          this.$bvToast.toast(`No found active user with email`, {
            title: "Error",
            variant: "danger",
            solid: true,
            autoHideDelay: 5000,
          }),
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