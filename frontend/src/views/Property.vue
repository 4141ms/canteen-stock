<template>
    <div>
        <el-container>
        
    <el-main>
        <el-table :data="orders" style="width: 100%" row-key="id">
            <el-table-column prop="id" label="编号" width="100">
                <template scope="scope"> {{ scope.row.index }}</template>
            </el-table-column>
            <el-table-column prop="name" label="用户名" min-width="100">
                <template scope="scope"> {{ scope.row.username }}</template>
            </el-table-column>
            <el-table-column prop="price" label="创建时间" min-width="100">
                <template scope="scope"> {{ scope.row.time }}</template>
            </el-table-column>
            <el-table-column prop="price" label="总额" width="100">
                <template scope="scope"> {{ scope.row.total }}</template>
            </el-table-column>
            <el-table-column label="操作" width="300" align="center">
                <template slot-scope="scope">
                    <!-- <el-button type="success" @click="handleEdit(scope.row)">详情 <i class="el-icon-edit"></i></el-button> -->
                    <el-popconfirm class="ml-5" confirm-button-text='确定' cancel-button-text='我再想想' icon="el-icon-info"
                        icon-color="red" title="您确定删除吗？" @confirm="del(scope.row.id)">
                        <el-button type="danger" slot="reference">删除 <i class="el-icon-remove-outline"></i></el-button>
                    </el-popconfirm>
                </template>
            </el-table-column>
        </el-table>
    </el-main>
    <el-footer>
        <el-card>
            总营业额：{{ total }} 元
        </el-card>
    </el-footer>
    </el-container>
    </div>
</template>
<script>
export default {
    name: "Property",
    data(){
        return {
            orders: [],
            dialogFormVisible: false,
            form: {},
            total: 0
        }
    },
    methods: {
        getJson: function () {
            let that = this
            this.Request.get("property/showOrder/").then(function (ret) {
                //ajax请求发送成功后获取的请求
                that.orders = ret.data.orders;
                that.total = ret.data.total
                return ret.orders;

            }).catch(function (ret) {
                //失败或者异常之后的内容
                console.log(ret)
            })
        },
        handleEdit(row) {
            this.form = Object.assign({}, row)

            this.dialogFormVisible = true
        },
        handleAdd: function () {
            this.form = {}
            this.dialogFormVisible = true
        },
        del(id) {
            let that = this
            this.Request.post("property/delOrder/", id).then(function (res) {
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
        save: function () {
            // this.Request.post("property/editStock/", this.form).then(res => {
            //     if (res.data.code === 200) {
            //         this.getJson()
            //         this.dialogFormVisible = false
            //         this.$message.success("修改成功！")
            //     } else {
            //         this.$message.error("修改失败！")
            //     }
            // })
        }
    },
    mounted() {
        this.getJson();
    },
}

</script>