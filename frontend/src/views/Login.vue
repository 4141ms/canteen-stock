<template>
    <div class="wrapper">
      <div style="margin: 200px auto; background-color: #fff; width: 350px; height: 300px; padding: 20px; border-radius: 10px">
        <div style="margin: 20px 0; text-align: center; font-size: 24px;"><b>登录</b></div>
        <el-form :model="user" :rules="rules" ref="userForm">
          <!-- {% csrf_token %} -->
          <el-form-item prop="username">
            <el-input size="medium" style="margin: 10px 0" prefix-icon="el-icon-user" v-model="user.username"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input size="medium" style="margin: 10px 0" prefix-icon="el-icon-lock" show-password v-model="user.password"></el-input>
          </el-form-item>
          <div style="margin: 10px 0; text-align: right">
            <el-button type="primary" size="small" autocomplete="off" @click="login">登 录</el-button>
            <el-button type="warning" size="small" autocomplete="off" @click="$router.push('/register')">注 册</el-button>
          </div>
        </el-form>

      </div>
    </div>
</template>

<script>
import store from '../store';

import {setRoutes} from "@/router";

export default {
  name: "Login",
  data: ()=>({
    user: {},
    rules: {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur'},
        { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
      ],
    }
  }),
  methods: {
    login: function () {
      this.$refs['userForm'].validate((valid) => {
        if (valid) {  //表单校验合法
          this.Request.post("login/", this.user).then(res => {
            // console.log(res.data)
            if (res.data.code === 200) {
              // store.commit("clear")
              localStorage.setItem("user", JSON.stringify(res.data.user))  //存储用户信息到浏览器
              localStorage.setItem("menus", JSON.stringify(res.data.menus))  //存储用户管理的菜单信息到浏览器
              localStorage.setItem("role", res.data["role"])
              this.$message.success("登录成功")

              //动态设置当前用户的路由
              setRoutes()
              console.log("login", this.$router.getRoutes());
              this.$router.push("/home")
            } else {
              this.$message.error(res.msg)
            }
          }).catch(function(ret){
                //失败或者异常之后的内容
                console.log("登录失败")
          })

        }
      });

    }
  }
}
</script>

<style>
  .wrapper {
    height: 100vh;
    /*background-image: linear-gradient(to bottom right, #FC4668, #3F5EF8);*/
    /*background-image: linear-gradient(to bottom right, #6190E8, #A7BFE8);*/
    background-image: linear-gradient(to bottom right, #4DA2CB, #67B26F);
    overflow: hidden;
}
</style>