<template>
  <el-container>
    <el-main style="height: 700px;">

      <el-row style="flex: wrap; flex-direction: row">
        <el-col :span="5" v-for="(dish, index) in menus" :key="index" :offset="1">
          <el-card :body-style="{ padding: '0px' }">
            <el-image class="image"
              src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png">
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>

            <div style="padding: 14px;">
              <span>{{ dish.name }}</span>

              <div class="bottom clearfix">
                <time class="time">{{ currentDate }}</time>
                <el-button type="text" class="button">操作按钮</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
    <el-footer style="margin-top: 25px;">
      <el-card>

        菜品清单
      </el-card>
    </el-footer>
  </el-container>
</template>

<style>
.el-card:hover {
  margin-top: -5px;
}

.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both
}

.el-row {
  margin-bottom: 20px;

  &:last-child {
    margin-bottom: 0;
  }
}

.el-col {
  border-radius: 4px;
}

</style>
  
<script>
export default {
  name: 'Order',
  data() {
    return {
      menus: [],
      multipleSelection: [],
      currentDate: new Date()
    }
  },
  methods: {
    getJson: function () {
      let that = this
      this.Request.get("backend/show_menu/").then(function (ret) {
        //ajax请求发送成功后获取的请求
        that.menus = ret.data.menus;
        return ret.menus;

      }).catch(function (ret) {
        //失败或者异常之后的内容
        console.log(ret)
      })

    },
    handleSelectionChange(val) {
      console.log("here", val);
      this.multipleSelection = val
    },
  },
  created() {
    this.getJson();
  }
}
</script>
  