import Vue from 'vue';
import Router from 'vue-router';
import VueQrcodeReader from 'vue-qrcode-reader';

import store from '../store/index';

Vue.use(VueQrcodeReader);
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: require('@/components/Login/Login').default,
      beforeEnter: (to, from, next) => {
        if (!store.getters['User/IS_LOGGED_IN']) {
          next();
        } else {
          next({ name: 'priority' });
        }
      },
    },
    {
      path: '/priority',
      name: 'priority',
      component: require('@/components/Priority/Priority').default,
      beforeEnter: (to, from, next) => {
        if (store.getters['User/IS_LOGGED_IN']) {
          next();
        } else {
          next({ name: 'login' });
        }
      },
    },
    {
      path: '/logout',
      name: 'logout',
      component: require('@/components/Logout').default,
      beforeEnter: (to, from, next) => {
        if (store.getters['User/IS_LOGGED_IN']) {
          next();
        } else {
          next(from);
        }
      },
    },
    {
      path: '*',
      redirect: '/',
    },
  ],
});
