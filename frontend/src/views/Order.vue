<template>
    <el-table
      :data="menus"
      style="width: 100%">
      <el-table-column
        prop="id"
        label="编号"
        min-width="100">
        这是order组件
        <template scope="scope"> {{ scope.row.pk }}</template>
      </el-table-column>
      <el-table-column
        prop="name"
        label="菜名"
        width="100">
        <template scope="scope"> {{ scope.row.fields.name }}</template>
      </el-table-column>
      <el-table-column
        prop="price"
        label="价格"
        width="100">
        <template scope="scope"> {{ scope.row.fields.price }}</template>
      </el-table-column>
    </el-table>
</template>
  
  <script>
  export default {
    name: 'Order',
    data () {
      return {
        menus: []
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
            
        }
    },
    created() {
        this.getJson();
    }
}
  </script>
  