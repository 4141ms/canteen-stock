import Vue from 'vue'
import Vuex from 'vuex'
import router, {resetRouter} from "@/router";

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        currentPathName: ''
    },
    mutations: {
        setPath (state) {
            state.currentPathName = localStorage.getItem("currentPathName")
        },
        logout: function () {
            //清空缓存
            localStorage.removeItem("user")
            localStorage.removeItem("menus")
            localStorage.removeItem("role")
            router.push("/login")

            //重置路由
            resetRouter()

        },
        clear: ()=>{
            localStorage.removeItem("user")
            localStorage.removeItem("menus")
            localStorage.removeItem("role")
        }
    }
})

export default store