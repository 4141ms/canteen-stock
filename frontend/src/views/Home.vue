<template>
  <div>
    <!-- 这是Home组件 -->
    <el-row :gutter="10" style="margin-bottom: 80px">
      
      <el-col :span="6">
        <el-card style="color: #409eff">
          <div><i class="el-icon-user-solid" />用户总数</div>
          <div style="padding: 10px 0; text-align: center; font-weight: bold">
            {{userNum}}
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card style="color: #f56c6c">
          <div><i class="el-icon-money" />管理员总数</div>
          <div style="padding: 10px 0; text-align: center; font-weight: bold">
            {{adminNum}}
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card style="color: #67C23A">
          <div><i class="el-icon-bank-card" />顾客总数</div>
          <div style="padding: 10px 0; text-align: center; font-weight: bold">
            {{cusNum}}
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card style="color: #e6a23c">
          <div><i class="el-icon-s-shop" />角色总数</div>
          <div style="padding: 10px 0; text-align: center; font-weight: bold">
            {{roleNum}}
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row style="display: flex">
      <el-col :span="12">
        <div id="pie" style="width: 450px; height: 400px"></div>
      </el-col>
      <el-col :span="12">
        <div id="pieUser" style="width: 450px; height: 400px; "></div>
      </el-col>
      <el-col :span="12">
        <div id="main" style="width: 450px; height: 400px"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: "Home",
  data: () => ({
    userNum: 8,
    adminNum: 5,
    cusNum: 5,
    roleNum: 2,
  }),
  mounted() { //页面元素渲染之后再触发
    var option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      title: {
        text: '菜品下单量',
        subtext: '柱状图',
        left: 'right'
      },
      xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        axisTick: {
          alignWithLabel: true
        },
        axisLabel: {
          rotate:36,
          interval:0,
          fontSize: "10",
        }
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '数量',
          data: [15, 20, 12, 30, 45, 26],
          type: 'bar',
          barWidth: '60%',
          showBackground: true,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0, // 若将此值设为1，表示从右到左渐变
              y: 1, // 若将此值设为1，表示从上到下渐变
              x2: 0, // 左
              y2: 0, // 上
              colorStops: [
                {
                  offset: 0,
                  color: '#192060' // 0% 处的颜色
                },
                {
                  offset: 0.9,
                  color: '#00C0FF' // 90% 处的颜色
                }
              ]
            }
          }
        }
      ],

    };
    //饼图
    var pieOption = {
      title: {
        text: '库存余量图',
        subtext: '比例图',
        left: 'center'
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: "菜品",
          type: 'pie',
          radius: '50%',
          // center: ['25%', '50%'],
          label: {
            normal: {
              show: true,
              position: 'inner',
              textStyle: {
                fontWeight: 300,
                fontSize: 14,
                color: "#fff"
              },
              formatter: '{d}%'
            },
          },
          data: [   //填空
            { value: 1048, name: 'Search Engine' },
            { value: 735, name: 'Direct' },
            { value: 580, name: 'Email' },
            { value: 484, name: 'Union Ads' },
            { value: 300, name: 'Video Ads' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };

    var pieTurnover = {
      title: {
        text: '营业额占比统计',
        subtext: '比例图',
        left: 'right'
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: "营业额",
          type: 'pie',
          radius: '50%',
          center: ['70%', '50%'],
          label: {
            normal: {
              show: true,
              position: 'inner',
              textStyle: {
                fontWeight: 300,
                fontSize: 14,
                color: "#fff"
              },
              formatter: '{d}%'
            },
          },
          data: [   //填空
            {name: "第一季度", value: 5},
            {name: "第二季度", value: 6},
            {name: "第三季度", value: 7},
            {name: "第四季度", value: 8},
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };

    var chartDom = document.getElementById('main');
    var myChart = echarts.init(chartDom);

    var pieDom = document.getElementById('pie');
    var pieChart = echarts.init(pieDom);

    var pieUserDom = document.getElementById('pieUser');
    var pieUserChart = echarts.init(pieUserDom);

  //   // this.Request.get("/echarts/head").then(res => {
  //   //   if(res.code == '200') {
  //   //     this.userNum = res.data["userNum"]
  //   //     this.teacherNum = res.data["teacherNum"]
  //   //     this.studentNum = res.data["studentNum"]
  //   //     this.roleNum = res.data["roleNum"]

  //   //     this.$message.success("获取信息成功！")
  //   //   } else {
  //   //     this.$message.error("获取信息失败！")
  //   //   }
  //   // })

    this.Request.get("/backend/stock_map_data").then(res => {
      pieOption.series[0].data = res.data["pieData"]
      pieChart.setOption(pieOption)
    })

    this.Request.get("/backend/turnover_map_data").then(res => {
      console.log(res.data)
      pieTurnover.series[0].data = res.data["turnover"]
      pieUserChart.setOption(pieTurnover)
    })

    this.Request.get("/backend/dish_map_data").then(res => {
      console.log(res.data)
      option.xAxis.data = res.data["xlabel"]
      option.series[0].data = res.data["xdata"]
      myChart.setOption(option)
    })

  }
}
</script>

<style scoped>

</style>