<template>
    <div>
        <div style="margin: 10px 0; display:flex">
            <el-button type="primary" @click="handleAdd">新增</el-button>
            <el-button type="primary" @click="showSupplier">供货商列表</el-button>
            <download-excel :data='tableData' :fields='json_fields' :name='`${tableDataType}.xlsx`' style="margin-left: 8px;">
                <el-button type='primary'>导出 采购表</el-button>
            </download-excel>
            <div style="margin-left: 8px;">
                阈值：
            <el-input type="number" 
            style="width: 100px;" 
            label="阈值：" 
            v-model="threshold"
            suffix-icon="el-icon-set-up"></el-input>
            </div>
            
        </div>

        <el-table :data="stocks" style="width: 100%" row-key="id">
            <el-table-column prop="id" label="编号" width="100">
                <template scope="scope"> {{ scope.row.index }}</template>
            </el-table-column>
            <el-table-column prop="name" label="原料名" min-width="100">
                <template scope="scope"> {{ scope.row.name }}</template>
            </el-table-column>
            <el-table-column prop="price" label="价格" width="100">
                <template scope="scope"> {{ scope.row.price }}</template>
            </el-table-column>
            <el-table-column prop="price" label="库存" width="100">
                <template scope="scope">
                    <div v-if="scope.row.number <= threshold" style="color: red;">
                        {{ scope.row.number }}
                    </div>
                    <div v-if="scope.row.number > threshold">
                        {{ scope.row.number }}
                    </div>
                </template>
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

        <el-dialog title="管理原料" :visible.sync="dialogFormVisible" width="35%">
            <el-form label-width="100px" size="small">
                <el-form-item label="名称">
                    <el-input v-model="form.name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="价格">
                    <el-input v-model="form.price" autocomplete="off" type="number"></el-input>
                </el-form-item>
                <el-form-item label="数量">
                    <el-input v-model="form.number" autocomplete="off" type="number"></el-input>
                </el-form-item>
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="save">确 定</el-button>
            </div>
        </el-dialog>

        <el-dialog title="供货商列表" :visible.sync="dialogSupVisible" width="35%">
            <el-table :data="shoppers" style="width: 100%" row-key="id">
                <!-- <el-table-column prop="id" label="编号" width="100">
                    <template scope="scope"> {{ scope.row.fields.id }}</template>
                </el-table-column> -->
                <el-table-column prop="contact_name" label="供货商名" width="100">
                    <template scope="scope"> {{ scope.row.fields.contact_name }}</template>
                </el-table-column>
                <el-table-column prop="company_name" label="公司名" width="100">
                    <template scope="scope"> {{ scope.row.fields.company_name }}</template>
                </el-table-column>
                <el-table-column prop="contact_phone" label="电话" min-width="100">
                    <template scope="scope"> {{ scope.row.fields.contact_phone }}</template>
                </el-table-column>
            </el-table>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogSupVisible = false">关闭</el-button>
            </div>
        </el-dialog>
    </div>
</template>
<script>
export default {
    name: "Inventory",
    data() {
        return {
            stocks: [],
            shoppers: [],
            dialogFormVisible: false,
            form: {},
            threshold: 20,
            tableData: [],    // 存放用于导出excel的数据
            tableFilterData:[
                { label: '字段1', prop: 'rsName' },
                { label: '字段2', prop: 'rsCode' },
            ],
            tableDataType: "采购表",
            json_fields: {
                编号: "index",    //常规字段
                原料名: "name", //支持嵌套属性
                价格: "price",
                数量:"number"
            },
            dialogSupVisible: false
        }

    },
    methods: {
        getJson: function () {
            let that = this
            this.Request.get("property/showStock/").then(function (ret) {
                //ajax请求发送成功后获取的请求
                that.stocks = ret.data.stocks;
                that.tableData = ret.data.stocks.filter((m) => m.number <= that.threshold)
                console.log(that.tableData);
                console.log(that.stocks);
                return ret.stocks;

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
            this.Request.post("property/delStock/", id).then(function (res) {
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
            this.Request.post("property/editStock/", this.form).then(res => {
                if (res.data.code === 200) {
                    this.getJson()
                    this.dialogFormVisible = false
                    this.$message.success("修改成功！")
                } else {
                    this.$message.error("修改失败！")
                }
            })
        },
        // 动态配置导出Excel文件的表头
        exportExcelHeader() {
            this.json_fields = {};
            this.tableFilterData.forEach(e => {
                this.json_fields[e.label] = e.prop;
            });
        },
        showSupplier() {
            let that = this
            this.Request.get("property/suppliers/").then(function (ret) {
                //ajax请求发送成功后获取的请求
                that.shoppers = ret.data.suppliers;
                console.log(ret.data.suppliers);
                that.dialogSupVisible = true
                return ret.shoppers;

            }).catch(function (ret) {
                //失败或者异常之后的内容
                console.log(ret)
            })
            
        }
    },
    mounted() {
        this.getJson();
    },
    watch:{
        threshold(){
            this.tableData = this.stocks.filter((m) => m.number <= this.threshold)
        }
    }
}

</script>