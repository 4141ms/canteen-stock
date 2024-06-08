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
        <template scope="scope"> {{ scope.row.id }}</template>
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
        <el-form-item label="原料">
          <el-button type="primary" @click="editRaw(form.raw)">编辑</el-button>
          <el-table :data="form.raw" style="width: 100%" row-key="raw_id">
            <el-table-column prop="name" label="原料" min-width="100">
              <template scope="scope"> {{ scope.row.name }}</template>
            </el-table-column>
            <el-table-column prop="price" label="数量(份)" width="100">
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
      
      <el-form-item v-for="(raw, index) in rawFrom.raws" label="原料:" :key="index">
        <el-row :gutter="10">
          <el-col :span="10">
            <el-select v-model="raw.name">
              <el-option
                v-for="item in options"
                :key="item.id"
                :label="item.name"
                :value="item.name">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-input  type="number" v-model="raw.number"></el-input>
          </el-col>
          <el-button @click.prevent="removeRaw(raw)">删除</el-button>
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
          value: '',
          number: 1
        }],
      },
      options:[
        {
          id:1,
          name: "牛肉",
        },
        {
          id:2,
          name:"米"
        }
      ]
    }
  },
  methods: {
    getJson: function () {
      let that = this
      this.Request.get("show_menu/").then(function (ret) {
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

    },
    handleEdit(row) {
      this.form = Object.assign({}, row)

      this.dialogFormVisible = true
    },
    del(id) {
      console.log("删除");
      // this.Request.delete("/menu/"+ id).then(res => {
      //   if(res.code == '200') {
      //     this.$message.success("删除成功！")
      //     this.load()
      //   } else {
      //     this.$message.error("删除失败！")
      //   }
      // })
    },
    editRaw: function (row){
      this.rawFrom.raws = Object.assign([], row)
      this.dialogRawVisible = true
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert('submit!');
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    removeRaw(item) {
      var index = this.rawFrom.raws.indexOf(item)
      if (index !== -1) {
        this.rawFrom.raws.splice(index, 1)
      }
    },
    addRaw() {
      this.rawFrom.raws.push({
        value: '',
        key: Date.now()
      });
    },
    getRawOption(){

    }
  },
  created() {
    this.getJson();
    // 获取原料列表
    this.getRawOption();
  }
}
</script>
  
<style>
.headerBg {
  background-color: #eee !important;
}
</style>