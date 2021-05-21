<template>
  <div class="mt-5">
    <b-container>
      <h5>Select a category:</h5>
      <b-form-select
        v-model="selected"
        :options="allCategories"
        value-field="id"
        text-field="title"
        class="mb-3"
      ></b-form-select>
      <b-card
        id="table"
        class="mb-2"
        v-for="(course, id) in courses"
        :key="id"
        bg-variant="default"
        text-variant="dark"
        :title="course.title"
      >
        <b-card-text>
          {{ course.description }}
        </b-card-text>
        <b-button variant="primary" @click="onClick(course.id)"
          >More info</b-button
        >
      </b-card>
      <div class="overflow-auto">
        <b-pagination
          v-model="currentPage"
          :total-rows="countOfCourses"
          :per-page="perPage"
          aria-controls="table"
          @change="getCoursesPage"
        ></b-pagination>
      </div>
    </b-container>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  name: "Courses",
  data() {
    return {
      perPage: 3,
      pageOffset: 0,
      currentPage: 1,
      selected: "",
      value: 1,
    };
  },
  methods: {
    getCoursesPage(value) {
      this.currentPage = value;
      this.pageOffset = this.perPage * (this.currentPage - 1);
      this.$store.dispatch("getCourses", {
        limit: this.perPage,
        offset: this.pageOffset,
        category: this.selected,
      });
    },
    onClick(value) {
      this.$router.push(`/course/${value}/promo`);
    },
  },
  mounted() {
    this.$store.dispatch("getCourses", {
      limit: this.perPage,
      offset: this.pageOffset,
      category: this.selected,
    });
    this.$store.dispatch("getCategories");
  },
  watch: {
    selected: function () {
      this.getCoursesPage(this.value);
    },
  },
  computed: {
    ...mapGetters(["courses", "countOfCourses", "categories"]),
    allCategories() {
      let result = [{ id: "", title: "All" }];
      return result.concat(this.categories);
    },
  },
};
</script>