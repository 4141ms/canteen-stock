// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import router from './router'
import store from "@/store";
import axios from 'axios'
import request from "@/utils/request";

Vue.config.productionTip = false
Vue.use(ElementUI, {size:"mini"});
// 全局注册
Vue.prototype.$axios = axios
Vue.prototype.$url = 'http://127.0.0.1:8000/backend/';
Vue.prototype.Request = request

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
