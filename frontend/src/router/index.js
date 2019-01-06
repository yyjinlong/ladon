import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import STree from '@/components/STree'
import Admin from '@/components/Admin'
import Help from '@/components/Help'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      redirect: '/stree',
      children: [
        {path: 'stree', name: 'stree', component: STree},
      ]
    },
    {
      path: '/',
      name: '',
      component: Home,
      children: [
        {path: 'admin', name: 'admin', component: Admin},
        {path: 'help', name: 'help', component: Help}
      ]
    }
  ],
  mode: 'history'
})
