<template>
  <div>
    <div id="site-navbar">
      <div class="container">
        <div class="navbar-image">
          <img class="navbar-image" src="../assets/img/logo.png" height="24px" alt="noline">
        </div>
        <input class="navbar-button border white" type="button" name="sign-in" value="Sign in">
        <input class="navbar-button white" type="button" name="join-us" value="Join us">
      </div>
    </div>
    <div class="img-container">
      <img class="bg-img" src="../assets/img/bg.png">
    </div>
    <section id="register-feed">
      <div class="form">
        <div class="input-form">
          <div class="main-description">Provide a better customer experience</div>
          <small class="secondary-description">Just a few steps to get you started</small>
          <form class="register-card">
            <div class="floating-placeholder">
              <label for="name">Company Name</label>
              <input v-model="companyName" class="light" type="text"/>
              <label for="email">Email Address</label>
              <input v-model="email" class="light" name="name" type="text"/>
              <label for="username">Username</label>
              <input v-model="username" class="light" name="name" type="text"/>
              <label for="password">Password</label>
              <input v-model="password" class="light" name="name" type="text"/>
              <label for="password1">Confirm Password</label>
              <input v-model="confirmPassword" class="light" name="name" type="text"/>
              <div class="submit-form">
              <button
                type="button"
                class="blue large btn-submit"
                @click="register"
              >
                SIGN IN
              </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>
  </div>
</template>

<style lang="scss" scoped>
@import "../assets/sass/styles.scss";
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      companyName: '',
      email: '',
      username: '',
      password: '',
      confirmPassword: '',
    };
  },

  methods: {
    register() {
      axios.post('API_URL_HERE', {
        company_name: this.companyName,
        email: this.email,
        username: this.username,
        password: this.password,
      }).then((response) => {
        console.log(response);
        if (response.data.message === 'Successful') {
          this.$router.push('/login');
        }
      });
    },
  },
};
</script>
