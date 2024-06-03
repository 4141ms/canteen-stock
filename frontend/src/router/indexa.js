import Vue from 'vue'
import VueRouter from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import store from "@/store";

Vue.use(VueRouter)

// export default new VueRouter({
//   routes: [
//     {
//       path: '/',
//       name: 'Menu',
//       component: () => import('../views/Menu.vue')
//     },
//     {
//       path: '/login',
//       name: 'Login',
//       component: () => import('../views/Login.vue')
//     },
//     // {
//     //   path: '/',
//     //   name: 'Register',
//     //   component: () => import('../views/Register')
//     // },
//     {
//       path: '/register',
//       name: 'Register',
//       component: () => import('../views/Register')
//     }
//   ]
// })

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  // {
  //   path: '/register',
  //   name: 'Register',
  //   component: () => import('../views/Register.vue')
  // },
  {
    path: '/404',
    name: '404',
    component: () => import('../views/404.vue')
  },
  {
    path: '/menu',
    name: 'Menu',
    component: () => import('../views/menu.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// 提供一个重置路由的方法
export const resetRouter = () => {
  router.matcher = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
  })
}

export const setRoutes = () => {
  const storeMenus = localStorage.getItem("menus");
  if (storeMenus) {
    //获取当前的路由对象名称数组
    const currentRouteNames = router.getRoutes().map(v => v.name)
    if (!currentRouteNames.includes('Manage')) {
      console.log("here2");
      //拼装动态路由
      const manageRoute = {
        path: '/', name: "Manage", component: () => import('../views/Manage.vue'), redirect: "/home", children: [
          { path: 'person', name: '个人信息', component: () => import('../views/Person.vue') },
        ]
      }
      console.log("here2", manageRoute);
      const menus = JSON.parse(storeMenus)
      menus.forEach(item => {
        if (item.path) {  //当且仅当path不为空的时候才去设置路由
          let t_path = item.path.replace("/", "")
          let tmp_path = t_path.replace(t_path[0],t_path[0].toUpperCase());
          let itemMenu = { path: item.path.replace("/", ""), name: item.name, component: () => import('../views/' + tmp_path + '.vue') }
          manageRoute.children.push(itemMenu)
        } 
      })
      //动态添加到现在的路由对象中去
      router.addRoute(manageRoute)
      console.log("router.addRoute(manageRoute):" ,manageRoute);
      console.log("router.getRoutes():", router.getRoutes());
    }

  }
}

setRoutes()


// 路由守卫
router.beforeEach((to, from, next) => {
  localStorage.setItem("currentPathName", to.name) //设置当前的路由名称，为了在Header组件中去使用
  console.log("from.name", from.name)
  console.log("to.name", to.name)
  store.commit("setPath") //触发store的数据更新
  
  console.log("to.matched",to.matched);
  //未找到路由的情况
  if (!to.matched.length) {
    const storeMenus = localStorage.getItem("menus")
    console.log("storeMenus", storeMenus)
    if (storeMenus) {
      next("/404")  //放行路由
    } else {
      //跳回登录界面
      next("/login")
    }
  }
  console.log("router", router.getRoutes());

  //其他情况直接放行
  next()
  
})

export default router


