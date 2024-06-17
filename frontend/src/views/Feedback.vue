<template>
    <div>
        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>反馈信息</span>
                <el-button style="float: right; padding: 3px 0" type="text" @click="handleAdd">评论</el-button>
            </div>
            <div v-for="fb in feedbacks" :key="fb.feedback_id" class="text item">
                <el-row>
                    <div>{{ fb.form.username }}</div>
                    <div>{{'评论 ' + fb.form.content }}</div>
                    
                    <el-button type="success" @click="edit_feedback(form.content)">编辑 <i class="el-icon-edit"></i></el-button>
                    <el-popconfirm class="ml-5" confirm-button-text='确定' cancel-button-text='我再想想' icon="el-icon-info"
                        icon-color="red" title="您确定删除吗？" @confirm="del_feedback(scope.row.id)">
                        <el-button type="danger" slot="reference">删除 <i class="el-icon-remove-outline"></i></el-button>
                    </el-popconfirm>
                </el-row>
            </div>
        </el-card>

        <el-dialog title="填写评论" :visible.sync="dialogFormVisible" width="35%">
            <el-form label-width="100px" size="small">
                <el-input v-model="form.name" autocomplete="off"></el-input>
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="edit_feedback">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>
<script>
export default {
    name: "Feedback",
    data(){
        return {
            feedbacks: [],
            form: {},
            dialogFormVisible: false
        }
    },
    methods: {
        getJson: function () {
            let that = this
            this.Request.get("/feedback/feedback_list/").then(function (ret) {
                //ajax请求发送成功后获取的请求
                that.feedbacks = ret.data.feedbacks;
                console.log(that.feedbacks);
                return ret.feedbacks;

            }).catch(function (ret) {
                //失败或者异常之后的内容
                console.log(ret)
            })
        },
        // 新增评论
        create: function () {
            let that = this
            this.Request.get("/feedback/create_feedback/").then(function (ret) {
                //ajax请求发送成功后获取的请求
                that.feedbacks = ret.data.feedbacks;
                return ret.feedbacks;

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
        // 编辑评论
        edit_feedback() {
            this.Request.post("/feedback/update_feedback/", this.form).then(res => {
                if (res.data.code === 200) {
                this.getJson()
                this.dialogFormVisible = false
                this.$message.success("修改成功！")
                } else {
                this.$message.error("修改失败！")
                }
            })
        },
        // 删除评论
        del_feedback(feedback_id) {
            let that = this
            this.Request.post("/feedback/delete_feedback/", feedback_id).then(function (res) {
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
        
    }
}

</script>

<style>
.headerBg {
  background-color: #eee !important;
}
</style>