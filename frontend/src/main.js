// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import router from './router'
import axios from 'axios'

Vue.use(ElementUI)
Vue.config.productionTip = false
// 全局注册
Vue.prototype.$axios = axios
Vue.prototype.$url = 'http://127.0.0.1:8000/backend/';
// Vue.config.globalProperties.$axios = axios;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
