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

    <el-table
      :data="menus"
      style="width: 100%"
      row-key="id">
      <el-table-column
        prop="id"
        label="编号"
        width="100">
        <template scope="scope"> {{ scope.row.pk }}</template>
      </el-table-column>
      <el-table-column
        prop="name"
        label="菜名"
        min-width="100">
        <template scope="scope"> {{ scope.row.fields.name }}</template>
      </el-table-column>
      <el-table-column
        prop="price"
        label="价格"
        width="100">
        <template scope="scope"> {{ scope.row.fields.price }}</template>
      </el-table-column>
      <el-table-column label="操作" width="300" align="center">
        <template slot-scope="scope">
          <el-button type="success" @click="handleEdit(scope.row)">编辑 <i class="el-icon-edit"></i></el-button>
          <el-popconfirm
              class="ml-5"
              confirm-button-text='确定'
              cancel-button-text='我再想想'
              icon="el-icon-info"
              icon-color="red"
              title="您确定删除吗？"
              @confirm="del(scope.row.pk)"
          >
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
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </div>
    </el-dialog>



  </div>
</template>
  
  <script>
  export default {
    name: 'Menu',
    data () {
      return {
        menus: [],
        dialogFormVisible: false,
        form: {},
        formLabelWidth: '120px',
      }
    },
    methods: {
        getJson: function (){
            let that = this
            this.Request.get("show_menu/").then(function(ret){
                //ajax请求发送成功后获取的请求
                    that.menus = ret.data.menus;
                    return ret.menus;
                
                }).catch(function(ret){
                //失败或者异常之后的内容
                    console.log(ret)
                })
            
        },
        handleAdd: function (){
          this.dialogFormVisible=true
          console.log("here");
        },
        save: function (){

        },
        handleEdit(row) {
          console.log("编辑");
          this.form = Object.assign({},row)
          console.log(this.form);
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
    },
    created() {
        this.getJson();
    }
}
  </script>
  
<style>
.headerBg {
  background-color: #eee !important;
}

</style>