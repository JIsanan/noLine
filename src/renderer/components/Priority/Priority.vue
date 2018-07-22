<template>
  <div class='parent'>
      <div class='child ' id='box-shadow'>
          <div class='textStyle'>Now Serving</div>
          <div class='prio-container'>
              <p class='prioNumStyle'>32</p>
          </div>
          <div class='inputparent'>
              <button class='buttonComplete large'>COMPLETE</button>
              <button class='buttonSkip large'>CANCEL</button>
          </div>
      </div>
      <router-link to="/logout">Logout</router-link>
  </div>
</template>

<style lang="scss" scoped>
@import "../../assets/sass/styles.scss";
</style>
