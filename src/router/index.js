import Vue from 'vue';
import Router from 'vue-router';
import About from '@/components/About';
import Register from '@/components/Register';
import Service from '@/components/Service';
import InQueue from '@/components/InQueue';
import CheckQueue from '@/components/CheckQueue';
import SMSNotif from '@/components/SMSNotif';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/about',
      name: 'about',
      component: About,
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
    },
    {
      path: '/inqueue',
      name: 'inqueue',
      component: InQueue,
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
