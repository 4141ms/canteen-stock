### 视频录制顺序
1. 项目启动
2. 登录注册（最后演示的时候用 admin账号）
3. 展示个人信息，退出（展示一下就行）
4. 菜单管理
   - 增加、删除菜单
   - 修改菜单，更改图片
   - 原料管理，增加、修改菜品对应的原料
5. 订餐管理：点餐操作，提交订单
6. 财产管理：查看刚刚增加的订单，删除刚刚增加的订单。营业总额改变
7. 库存管理：
    - 再新增一份订单，后查看库存的变化
    - 新增原料：菜单管理中的原料列表会发生改变。编辑原料：
    - 设置阈值，少于一定阈值原料标红
    - 导出标红原料的采购表
    - 展示供货商列表
8. 反馈信息：演示一下反馈信息的功能



### 订餐补货管理系统
前后端分离开发，使用git进行代码托管并协作开发

项目功能展示: https://www.bilibili.com/
### 前端
- nodejs
- 框架：vue2 cli+js
- 可视化：echarts
- 请求: axios
- UI库: element-ui
### 后端
- 框架: django
- 数据库: django自带的splite

### 项目启动方法
1. 将项目下载或clone到本地
2. 后端启动
   - 安装django环境
   - 在主目录下执行`"python manage.py runserver"`
3. 前端启动
   - cd 到frontend目录下
   - 安装nodejs
   - 执行命令`"npm install"`
   - 执行命令`"npm run dev"`
   - 在浏览器中输入url`"http://localhost:8080/login"`。
     如果登录后成功后跳转到404界面，直接再输入url`"http://localhost:8080/"`


