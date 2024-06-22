<template>
    <div>
        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>反馈信息</span>
                <el-button style="float: right; padding: 3px 0" type="text" @click="handleAdd">评论</el-button>
            </div>
            <div v-for="fb in fbList" :key="fb.pk" class="text item">
                <el-row style="margin-bottom: 5px; padding: 10px; background-color: #f5f5f5;">
                    <el-col :span="20">
                        <div style="margin-bottom: 5px;">{{ fb.fields.user_name }}</div>
                        <div style="margin-bottom: 10px; font-size: 12px;">{{ fb.fields.created_at }}</div>
                        <div style="">{{ fb.fields.content }}</div>
                    </el-col>
                    <el-col :span="4">
                        <el-button type="success" @click="handleEdit(fb.pk)">编辑 <i class="el-icon-edit"></i></el-button>
                        <el-popconfirm class="ml-5" confirm-button-text='确定' cancel-button-text='我再想想' icon="el-icon-info"
                            icon-color="red" title="您确定删除吗？" @confirm="del_feedback(fb.pk)">
                            <el-button type="danger" slot="reference">删除 <i class="el-icon-remove-outline"></i></el-button>
                        </el-popconfirm>
                    </el-col>
                </el-row>
            </div>
        </el-card>

        <el-dialog title="填写评论" :visible.sync="dialogFormVisible" width="35%">
            <el-form label-width="100px" size="small">
                <el-input v-model="form.content" autocomplete="off"></el-input>
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
            feedback: {},
            fbList: [],
            form :{},
            fb_id: -1,
            dialogFormVisible: false
        }
    },
    methods: {
        getJson: function () {
            let that = this
            this.Request.get("feedback/feedback_list/").then(function (ret) {
                //ajax请求发送成功后获取的请求
                console.log("here::::",ret);
                that.fbList = ret.data.feedbacks;
                console.log(that.fbList);
                
                for(let i in that.fbList) {
                    let time = that.fbList[i].fields.created_at
                    let date = new Date(time);

                    let year = date.getFullYear();
                    let month = String(date.getMonth() + 1).padStart(2, '0');
                    let day = String(date.getDate()).padStart(2, '0');
                    let hours = String(date.getHours()).padStart(2, '0');
                    let minutes = String(date.getMinutes()).padStart(2, '0');
                    let seconds = String(date.getSeconds()).padStart(2, '0');
                    
                    that.fbList[i].fields.created_at = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
                }
                return ret.fbList;
            }).catch(function (ret) {
                //失败或者异常之后的内容
                console.log(ret)
            })
        },
        handleEdit(row) {
            this.fb_id = row
            this.dialogFormVisible = true
        },
        handleAdd: function () {
            this.form = {}
            this.dialogFormVisible = true
        },
        // 新建或编辑评论
        edit_feedback(data) {
            if(this.fb_id != -1) {  // feedback_id存在，编辑评论
                console.log("fb_id", this.fb_id);
                this.Request.post("feedback/update_feedback/", {
                    feedback_id: this.fb_id,    
                    content: this.form.content
                }).then(res => {
                    console.log(res);
                    if (res.data.code === 200) {
                        this.fb_id = -1
                        this.getJson()
                        this.dialogFormVisible = false
                        this.$message.success("修改成功！")
                    } else {
                        this.$message.error("修改失败！")
                    }
                })
            } else {
                this.Request.post("feedback/create_feedback/", {
                        user_name: JSON.parse(localStorage.getItem("user")).username,
                        user_id: JSON.parse(localStorage.getItem("user")).id,
                        content: this.form.content,
                }).then(res => {
                console.log(res);
                if (res.data.code === 201) {
                    this.getJson()
                    this.dialogFormVisible = false
                    this.$message.success("创建成功！")
                } else {
                    this.$message.error("创建失败！")
                }
            })
            }
                
        },
        // 删除评论
        del_feedback(row) {
            this.fb_id = row
            let that = this
            this.Request.post("feedback/delete_feedback/",{
                feedback_id: this.fb_id
            }).then(function (res) {
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
        
    },
    mounted() {
        this.getJson()
    }
}
</script>

<style>
.headerBg {
  background-color: #eee !important;
}
</style>