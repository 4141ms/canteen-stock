<template>
  <div>
    <div style="margin: 10px 0">
      <el-button type="primary" @click="handleAdd">新增</el-button>
      <!-- <el-popconfirm
          class="ml-5"
          confirm-button-text='确定'
          cancel-button-text='我再想想'
          icon="el-icon-info"
          icon-color="red"
          title="您确定批量删除这些数据吗？"
          @confirm="delBatch"
      >
        <el-button type="danger" slot="reference">批量删除<i class="el-icon-remove-outline"></i></el-button>
      </el-popconfirm> -->
    </div>

    <el-table :data="menus" style="width: 100%" row-key="id">
      <el-table-column prop="id" label="编号" width="100">
        <template scope="scope"> {{ scope.row.index }}</template>
      </el-table-column>
      <el-table-column prop="name" label="菜名" min-width="100">
        <template scope="scope"> {{ scope.row.name }}</template>
      </el-table-column>
      <el-table-column prop="price" label="价格" width="100">
        <template scope="scope"> {{ scope.row.price }}</template>
      </el-table-column>
      <el-table-column label="操作" width="300" align="center">
        <template slot-scope="scope">
          <el-button type="success" @click="handleEdit(scope.row)">编辑 <i class="el-icon-edit"></i></el-button>
          <el-popconfirm class="ml-5" confirm-button-text='确定' cancel-button-text='我再想想' icon="el-icon-info"
            icon-color="red" title="您确定删除吗？" @confirm="del(scope.row.id)">
            <el-button type="danger" slot="reference">删除 <i class="el-icon-remove-outline"></i></el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="管理菜单" :visible.sync="dialogFormVisible" width="35%">
      <el-form label-width="100px" size="small">
        <el-form-item label="名称">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="价格">
          <el-input v-model="form.price" autocomplete="off" type="number"></el-input>
        </el-form-item>
      <el-form-item label="图片">
        <el-upload
          class="avatar-uploader"
          action="http://localhost:8000/backend/load_dish/"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
      >
        <img v-if="form.avatar_url" :src="form.avatar_url" class="avatar">
        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
    </el-form-item>
        <el-form-item label="原料">
          <el-button type="primary" @click="editRaw(form.raw)">编辑</el-button>
          <el-table :data="form.raw" style="width: 100%" row-key="raw_id">
            <el-table-column prop="name" label="原料" min-width="50">
              <template scope="scope"> {{ scope.row.name }}</template>
            </el-table-column>
            <el-table-column prop="price" label="需要数量(份)" width="100">
              <template scope="scope"> {{ scope.row.number }}</template>
            </el-table-column>
          </el-table>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="管理原料" :visible.sync="dialogRawVisible" width="25%">
      <!-- 动态表单 -->
      <el-form :model="rawFrom" ref="rawFrom" label-width="80px" class="demo-dynamic">

        <el-form-item v-for="(raw) in rawFrom.raws" label="原料:" :key="raw.raw_id">
          <el-row :gutter="10">
            <el-col :span="10">
              <el-select v-model="raw.name">
                <el-option v-for="item in options" :key="item.id" :label="item.name" :value="item.name">
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-input type="number" v-model="raw.number" min=1></el-input>
            </el-col>
            <el-popconfirm class="ml-5" confirm-button-text='确定' cancel-button-text='我再想想' icon="el-icon-info"
              icon-color="red" title="您确定删除这条数据吗？" @confirm="removeRaw(raw)">
              <el-button type="danger" slot="reference">删除<i class="el-icon-remove-outline"></i></el-button>
            </el-popconfirm>
          </el-row>

        </el-form-item>
        <el-form-item>
          <el-button @click="addRaw">新增原料</el-button>
          <el-button @click="resetForm('rawFrom')">重置</el-button>
          <el-button type="primary" @click="submitForm('rawFrom')">确认</el-button>
          <el-button @click="dialogRawVisible = false">取 消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>

  
<script>
export default {
  name: 'Menu',
  data() {
    return {
      menus: [],
      dialogFormVisible: false,
      form: {},
      formLabelWidth: '120px',
      dialogRawVisible: false,
      rawFrom: {
        raws: [{
          raw_id: 0,
          name: '',
          number: 1
        }],
      },
      options: [
        {
          id: 1,
          name: "牛肉",
        },
      ]
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
    handleAdd: function () {
      this.form = {}
      this.dialogFormVisible = true
    },
    save: function () {
      console.log("save", this.form);
      this.Request.post("backend/edit_menu/", this.form).then(res => {
        if (res.data.code === 200) {
          this.getJson()
          this.dialogFormVisible = false
          this.$message.success("修改成功！")
        } else {
          this.$message.error("修改失败！")
        }
      })
    },
    handleEdit(row) {
      this.form = Object.assign({}, row)

      this.dialogFormVisible = true
    },
    del(id) {
      let that = this
      this.Request.post("backend/del_menu/", id).then(function (res) {
        if (res.data.code === 200) {
          that.$message.success("删除成功！")
          that.getJson()
        } else {
          that.$message.error("删除失败！")
        }

      }).catch(function (ret) {
        //失败或者异常之后的内容
        console.log(ret)
      })
    },
    editRaw: function (row) {
      this.rawFrom.raws = Object.assign([], row)
      this.dialogRawVisible = true
    },
    submitForm(formName) {
      let form = {
        id: this.form.id,
        raws: this.rawFrom.raws
      }
      if (this.form.id ===undefined){
        this.dialogRawVisible=false
        this.form.raw = this.rawFrom.raws
        return
      }
      let that = this
      this.Request.post("backend/edit_menu_raw/", form).then(res => {
        if (res.data.code === 200) {
          that.form.raw = res.data.data.raws
          this.$message.success("修改成功！")
          that.dialogRawVisible = false
        } else {
          this.$message.error("修改失败！")
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    removeRaw(item) {
      let that = this
      this.Request.post("backend/del_menu_raw/", item.raw_id).then(function (res) {
        if (res.data.code === 200) {
          that.$message.success("删除成功！")
          var index = that.rawFrom.raws.indexOf(item)
          if (index !== -1) {
            that.rawFrom.raws.splice(index, 1)
          }
          that.form.raw = that.rawFrom.raws
        } else {
          that.$message.error("删除失败！")
        }


      }).catch(function (ret) {
        //失败或者异常之后的内容
        console.log(ret)
      })

    },
    addRaw() {
      this.rawFrom.raws.push({
        number: 1,
        key: Date.now(),
      });
    },
    getRawOption() {
      let that = this
      this.Request.get("backend/raw_set/").then(function (ret) {
        //ajax请求发送成功后获取的请求
        that.options = ret.data.options;
        return ret.options;

      }).catch(function (ret) {
        //失败或者异常之后的内容
        console.log(ret)
      })
    },
    handleAvatarSuccess(res) {
      this.form.avatar_url = res;
    }
  },

  mounted() {
    this.getJson();
  },
  created() {
    // 获取原料列表
    this.getRawOption();
  }
}
</script>
  
<style>
.headerBg {
  background-color: #eee !important;
}
.avatar-uploader {
  /* text-align: center; */
  padding-bottom: 10px;
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 80px;
  height: 80px;
  line-height: 80px;
  /* text-align: center; */
}
.avatar {
  width: 80px;
  height: 80px;
  display: block;
}
</style>