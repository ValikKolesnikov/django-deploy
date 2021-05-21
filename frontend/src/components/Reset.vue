<template>
  <div id="form">
    <h3>Reset password</h3>
    <b-form @submit.prevent="onSubmit">
      <b-form-group
        id="input-group-1"
        label="Your new password:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="password"
          type="password"
          placeholder="Enter new password"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-2"
        label="Confirm new password:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          v-model="password_confirm"
          type="password"
          placeholder="Confirm new password"
          required
        ></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: "Reset",
  data() {
    return {
      password: "",
      password_confirm: "",
    };
  },
  methods: {
    onSubmit() {
      this.$store
        .dispatch("resetPasswordConfirm", {
          password: this.password,
          password_confirm: this.password_confirm,
          uid: this.$route.params.uid,
          token: this.$route.params.token,
        })
        .then(
          () => this.$router.push("/login"),
          () =>
            this.$bvToast.toast(
              `Something went wrong. Try to reset password again`,
              {
                title: "Error",
                variant: "danger",
                solid: true,
                autoHideDelay: 5000,
              }
            )
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