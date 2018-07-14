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
              <input id="name" class="light" name="name" type="text"/>
              <label for="email">Email Address</label>
              <input id="email" class="light" name="name" type="text"/>
              <label for="username">Username</label>
              <input id="username" class="light" name="name" type="text"/>
              <label for="password">Password</label>
              <input id="password" class="light" name="name" type="text"/>
              <label for="password1">Confirm Password</label>
              <input id="password1" class="light" name="name" type="text"/>
              <div class="submit-form">
              <button class="blue large btn-submit">  SIGN IN </button>
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
