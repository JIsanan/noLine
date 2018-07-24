<template>
 <div class='pickprocess-container'>
      <router-link class="tab-buttons now" tag="button" to="/smsnotif">
        <div class="tab-header">Start Lining Up</div>
        <div class="tab-body">You will be placed at the last in line.</div>
      </router-link>
      <router-link class="tab-buttons later" tag="button" to="/smsnotif">
        <div class="tab-header">Decide Later</div>
        <div class="tab-body">You may decide when to line up using our application.</div>
      </router-link>
</div>
</template>

<style lang="scss" scoped>
  @import "../assets/sass/styles.scss";
</style>
