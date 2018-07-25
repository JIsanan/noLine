import Vue from 'vue';
import Router from 'vue-router';
import Register from '@/components/Register';
import Service from '@/components/Service';
import InQueue from '@/components/InQueue';
import CheckQueue from '@/components/CheckQueue';
import SMSNotif from '@/components/SMSNotif';
import store from '../store/store';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'root',
      redirect: '/service',
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
    },
    {
      path: '/service',
      name: 'service',
      component: Service,
      beforeEnter: (to, from, next) => {
        store.commit('REMOVE_ALL');
        next();
      },
    },
    {
      path: '/inqueue',
      name: 'inqueue',
      component: InQueue,
      beforeEnter: (to, from, next) => {
        if (store.state.pk === -1) {
          next({ name: 'service' });
        } else if (store.state.lineLater.length === 0) {
          next({ name: 'checkqueue' });
        } else {
          next();
        }
      },
    },
    {
      path: '/checkqueue',
      name: 'checkqueue',
      component: CheckQueue,
    },
    {
      path: '/smsnotif',
      name: 'smsnotif',
      component: SMSNotif,
    },
  ],
});
