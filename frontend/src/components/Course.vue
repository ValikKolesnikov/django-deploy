<template>
  <div class="container mt-5">
    <div>
      <h3 align="center">{{ course.title }}</h3>
    </div>
    <hr />
    <div>
      <h3>About this course</h3>
      <p class="mt-5">{{ course.description }}</p>
    </div>
    <div>
      <h3 class="mt-5 mb-3">Course content</h3>
      <div v-for="lesson in course.lessons" :key="lesson.id">
        <h4>{{ lesson.position }}. {{ lesson.title }}</h4>
        <div v-for="step in lesson.steps" :key="step.id" class="ml-5">
          <h5>{{ step.position }}.{{ step.title }}</h5>
        </div>
      </div>
    </div>
    <div class="mt-5 mb-3" align="center">
      <b-button type="submit" variant="primary" @click="joinCourse"
        >Enroll</b-button
      >
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  name: "Course",
  props: ["id"],
  methods: {
    joinCourse() {
      if (!this.user) {
        this.$router.push({
          name: "login",
          query: { redirect: `/course/${this.id}/promo` },
        });
      } else {
        this.$store
          .dispatch("joinCourse", this.id)
          .then(() =>
            this.$bvToast.toast("You have already enrolled in this course", {
              title: "E-learning App",
              variant: "info",
              solid: true,
              autoHideDelay: 5000,
            })
          )
          .catch((error) =>
            this.$bvToast.toast(error.response.data["detail"], {
              title: "E-learning App",
              variant: "danger",
              solid: true,
              autoHideDelay: 5000,
            })
          );
      }
    },
  },
  mounted() {
    this.$store.dispatch("getCourse", this.id);
  },
  computed: {
    ...mapGetters(["course", "user"]),
  },
};
</script>
