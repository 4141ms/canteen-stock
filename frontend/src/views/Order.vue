<template>
  <el-container>
    <el-main style="height: 700px;">

      <el-row style="flex: wrap; flex-direction: row">
        <el-col :span="5" v-for="(dish, index) in menus" :key="index" :offset="1">
          <el-card :body-style="{ paddingTop: '0px' }">
            <el-image class="image" :src="dish.image">
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>

            <div style="padding: 14px;">
              <span>{{ dish.name }}</span>

              <div class="bottom clearfix">
                <span>{{ dish.price }} 元</span>
                <el-input-number class="button" v-model="dish.num" @change="handleChange(dish)" :min="0" :max="10"
                  placeholder="0"></el-input-number>
                <!-- <time class="time">{{ currentDate }}</time> -->
                <!-- <el-button type="text" class="button">+1</el-button> -->
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
    <el-footer style="margin-top: 25px;">
      <el-card>
        <el-row :gutter="20">
          <el-col :span="2">
            <div>
              菜品清单
              <i class="el-icon-food"></i>
            </div>
          </el-col>
          <el-col :span="18" >
            <el-row style="flex: wrap; flex-direction: row">
              <el-col :span="3" v-for="(dish, index) in dishSet" :key="index" >
                <span>{{ dish.name }}</span>
                <span>{{ dish.num }} 份</span>
              </el-col>
            <!-- </div> -->
          </el-row>
          </el-col>
          <el-col :span="4">
            <div>
              <i class="el-icon-bank-card"></i>
              总价: {{ total }} 元
              <el-button type="primary" @click="save">确 定</el-button>
            </div>
          </el-col>
        </el-row>



      </el-card>
    </el-footer>
  </el-container>
</template>

<script>
export default {
  name: 'Order',
  data() {
    return {
      menus: [],
      dishSet: [],
      total: 0,
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
      this.dishSet = val
    },
    handleChange(data) {
      let id = data.id
      let dish = this.dishSet.filter((m) => m.id == id)
      if (dish.length != 0) {
        dish[0]["num"] = data.num
      } else {
        this.dishSet.push({
          "id": id,
          "name": data.name,
          "num": data.num,
          "price": data.price
        })
      }

      let sum = 0
      this.dishSet.map((m)=>{
        sum+=m.price*m.num
      })
      this.total = sum
    },
    save: function() {
      
      console.log(JSON.parse(localStorage.getItem("user")).id)
      this.Request.post("property/newOrder/", {
        params:{
          id: JSON.parse(localStorage.getItem("user")).id,
          data: this.dishSet
        }
        
      }).then(res => {
        console.log(res);
        if (res.data.code === 200) {
        //   // this.getJson()
          this.$message.success("提交成功！")
        } else {
          this.$message.error("提交失败！")
        }
      })
    }
  },
  created() {
    this.getJson();
  },
}
</script>

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
  height: 200px;
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
  