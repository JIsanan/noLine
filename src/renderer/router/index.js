import Vue from 'vue';
import Router from 'vue-router';
import VueQrcodeReader from 'vue-qrcode-reader';

Vue.use(VueQrcodeReader);
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: require('@/components/Login/Login').default,
    },
    {
      path: '/priority',
      name: 'priority',
      component: require('@/components/Priority/Priority').default,
    },
    {
      path: '*',
      redirect: '/',
    },
  ],
});
