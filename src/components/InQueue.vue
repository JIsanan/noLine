<template>
 <div class='inqueue-container'>
  <div class="inqueue-card-container">
    <div class='mainItem4'>
        <p class='serviceStyle'>
          Issuance of SSS Card
        </p>
    </div>
    <div class='mainItem1'>
        <div class='ETAstyle'>
          <p class='label-text'>Estimated Service Time</p>
          <p class='data-text'>50 min.</p>
          <p class='label-text'>Priority Num #:</p>
          <p class='data-text last-child'>50</p>
        </div>
        <div class='QRstyle'>
          <img class="img-qr" src="../assets/img/qr.png">
        </div>
    </div>
  </div>
  <div class='mainItem3'>
      <button
        class="large inqueue-buttons left"
        @click="$router.push({ name: 'smsnotif' })"
      >
        BACK
      </button>
      <button class="large inqueue-buttons blue right">CONTINUE</button>
  </div>
</div>
</template>

<style lang="scss" scoped>
  @import "../assets/sass/styles.scss";
</style>
