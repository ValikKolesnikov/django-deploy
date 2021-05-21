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
      <b-form-group id="input-group-2" label="Your Email:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.email"
          type="email"
          placeholder="Enter email"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-3"
        label="Your First Name:"
        label-for="input-3"
      >
        <b-form-input
          id="input-3"
          v-model="form.first_name"
          placeholder="First Name"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-4"
        label="Your Last Name:"
        label-for="input-4"
      >
        <b-form-input
          id="input-4"
          v-model="form.last_name"
          placeholder="Last Name"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-5"
        label="Your Password:"
        label-for="input-5"
      >
        <b-form-input
          id="input-5"
          v-model="form.password"
          type="password"
          placeholder="Password"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-checkbox
        id="checkbox-1"
        v-model="form.is_teacher"
        name="checkbox-1"
        value="true"
        unchecked-value="false"
      >
        Are you a teacher?
      </b-form-checkbox>

      <b-button type="submit" variant="primary">Register</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        password: "",
        is_teacher: false,
      },
    };
  },
  methods: {
    onSubmit() {
      this.$store
        .dispatch("signUp", {
          username: this.form.username,
          first_name: this.form.first_name,
          last_name: this.form.last_name,
          email: this.form.email,
          password: this.form.password,
          is_teacher: this.form.is_teacher,
        })
        .catch(() =>
          this.$bvToast.toast(
            `User with that username or email already exists`,
            {
              title: "Error",
              variant: "danger",
              solid: true,
              autoHideDelay: 5000,
            }
          )
        )
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