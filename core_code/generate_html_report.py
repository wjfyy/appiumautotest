import os
from datetime import datetime
from .common import get_path

HTML_START = """
<!DOCTYPE html>

<head>
    <meta charset="UTF-8">
    <title>Mobile UI Auto Test Report</title>
    <script type="text/javascript" src="http://172.16.7.217:8088/static/js/vue/moment.js"></script>
    <script type="text/javascript" src="http://172.16.7.217:8088/static/js/vue/vue.js"></script>
    <script type="text/javascript" src="http://172.16.7.217:8088/static/js/vue/vue-router.js"></script>
    <script type="text/javascript" src="http://172.16.7.217:8088/static/js/vue/antd.js"></script>
    <script type="text/javascript" src="http://172.16.7.217:8088/static/js/vue/echarts.min.js"></script>
    <link rel="stylesheet" href="http://172.16.7.217:8088/static/css/antd.css">
    <script>
        Vue.use(antd);
    </script>
</head>
<style>
    .title{
        font-weight: 600;
        font-size: 16px;
        line-height: 50px;
    }
    .device_title{
        color: #660;
        margin: 10px 0;
    }
    .device_content{
        color: #607d8b;
        margin-left: 20px;
    }
    .module{
        margin: 10px 0px;
        color: #607d8b;
        border-bottom: 1px solid #DCDCDC;
        font-weight: 600;
    }
    .content{
        display: flex;
        margin: 0 25px 20px;
        height: calc(100vh - 105px);
    }
    .content-left{
        flex: 5 1 auto;
        border-right: 1px solid #dcdcdc;
        padding-right: 20px;
        margin-bottom: 40px;
        overflow-x: auto;
    }
    .content-right{
        flex: none;
        width: 300px;
    }
    .sta{
        flex: 1;
        display: flex;
        justify-content: center;
    }
    .sta ul{
        width: 270px;
        margin: auto 10px;
        list-style: none;
        padding: 0;
    }
    .sta li{
        display: flex;
        align-items: center;
        margin: 10px 0;
    }
    .sta .dot{
        border-radius: 50%;
        width: 10px;
        height: 10px;
    }
    .sta .error_type{
        margin-left: 10px;
        font-weight: 600;
    }
    .sta .error_rate{
        color: #666;
        font-style: italic;
        margin-left: 20px;
        width: 100px;
    }
    .sta .error_rate::before{
        content: "";
        width: 1px;
        background-color: #dcdcdc;
        height: 1em;
        display: inline-block;
        margin-right: 5px;
    }
    .sta .error_rate::after{
        content: "";
        width: 50px;
        border-top: 1px dotted #bfbfbf;
        height: 0;
        bottom: 5px;
        display: inline-block;
    }
    #sta{
        width: 200px ;
        height: 200px;
    }
    .sta_mouseover{
        position: absolute;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        bottom: 30%;
        left: 32%;
    }
    .ant-descriptions-item-label{
    font-size: 10px;
    }

</style>
"""


HTML_TITLE = """
<body>
    <h3>
        <img style="margin-left: 25px; vertical-align: baseline;" 
        src="http://172.16.7.217:8088/wisedu/test_platform/logo_img" alt="wisedu"/>
        <span style="font-weight: 600; font-size: 18px; vertical-align: super;">Mobile UI 自动化测试报告</span>
    </h3>
    <div style="height: 50px; 
    background-color: #f7f7f7; 
    border-top: 1px solid #DCDCDC;
    border-bottom: 1px solid #DCDCDC;">
        <span class="title" style="margin-left: 25px; ">项目名称：</span>
        <span class="title" >{project}</span>
    </div>

    <div id="app"></div>
    
<script>
"""

HTML_OVERVIEW = """
Vue.component('test_overview', {
    template:
    `
    <div style="min-width: 500px; flex: 1;">
        <ul style="margin-top: 0px;
        border: 1px solid #ddd;
        border-radius: 3px;
        padding: 10px;
        margin-bottom: 0px;
        margin-left: 0px;
        padding-left: 25px;
        background-color: #f6f6f6;">
            <li style="font-size: 15px;line-height: 1.6;">
                <span style="color: #660;">测试用例:</span>
                <span style="color: #607d8b;">%(case_count)s 条</span>
            </li>
            <li style="font-size: 15px;line-height: 1.6;">
                <span style="color: #660;">通过率:</span>
                <span style="color: #CDAD00;">%(pass_rate)s</span>
            </li>
            <li style="font-size: 15px;line-height: 1.6;">
                <span style="color: #660;">成功/失败:</span>
                <span style="color: #00CD66;">%(success)s</span>/<span style="color: red;">%(fail)s</span>
            </li>
            <li style="font-size: 15px;line-height: 1.6;">
                <span style="color: #660;">开始时间:</span>
                <span style="color: #607d8b;">%(start_time)s</span>
            </li>
            <li style="font-size: 15px;line-height: 1.6;">
                <span style="color: #660;">总耗时:</span>
                <span style="color: #607d8b;">%(exec_time)s s</span>
            </li>
        </ul>
        <p style="font-style: italic; font-size: 14px; color: #666; margin-top: 10px;">
            报告由Mobile UI 自动化测试框架自动生成。该报告只展示失败用例的详细信息
        </p>
        <p style="font-style: italic; font-size: 14px; color: #666; margin-top: 10px;">
            报告只能作为参考，实际产生的问题仍需进一步确认。
        </p>
    </div>
    `,
})
"""

HTML_DEVICE = """
Vue.component('device_info', {
    template:
    `
    <div class="content-right">
        <div style="margin-left: 20px;">
            <h2 class="module">设备信息</h2>
            <p class="device_title">操作系统</p>
            <span class="device_content">%(platform)s</span>
            <p class="device_title">系统版本</p>
            <span class="device_content">%(version)s</span>
            <p class="device_title">设备名称</p>
            <span class="device_content">%(device_name)s</span>
        </div>
    </div>
    `,
})
"""

HTML_STA1 = """
Vue.component('sta', {
    template:
    `
    <div class="sta">
        <div style="position: relative;">
            <div id="sta"></div>
            <div class="sta_mouseover">
                <div style="color: #409eff; font-size: 14px; text-align: center;">{{title}}</div>
                <div style="font-size: 14px; font-weight: 600; text-align: center">{{count}}</div>
            </div>
        </div>
        
        <ul>
            <li v-for="(color, idx) in option.color">
                <div class="dot" :style="{'background-color': color}"></div>
                <div class="error_type">{{option.series.data[idx].name}}</div>
                <div class="error_rate">{{option.series.data[idx].rate}}%</div>
                <div class="error_count">{{option.series.data[idx].value}}</div>
            </li>
        </ul>
    </div>         
    `,
    data(){
        return{
            init_title: '总失败数',
"""
HTML_STA2 = "init_count: %s,"
HTML_STA3 = """
            title: '',
            count: 0,
            chartDom: '',
            myChart: '',
            option: {
                    tooltip: {
                        show: false
                    },
                    color: ['#FFFF00', '#8B658B', '#FF0000', '#8B4513', '#00FF00'],
                    series: {
                            name: '访问来源',
                            type: 'pie',
                            radius: ['60%', '90%'],
                            label: {
                                show: false,
                                position: 'center'
                            },
                            emphasis: {
                                label: {
                                    show: false,
                                    fontSize: '16',
                                    fontWeight: 'bold'
                                }
                            },
                            labelLine: {
                                show: false
                            },
"""
HTML_STA4 = "data: %s"
HTML_STA5 = """
                           
                        }
                    
            },
        }
    },
    mounted(){
        this.chartDom = document.getElementById('sta');
        this.myChart = echarts.init(this.chartDom);
        this.myChart.setOption(this.option);
        this.title = this.init_title;
        this.count = this.init_count;
        this.myChart.on('mouseover',  (params)=> {
            this.title = params.name;
            this.count = params.percent;
        });
        this.myChart.on('mouseout',  ()=> {
            this.title = this.init_title;
            this.count = this.init_count;
        });
    }
})
"""

HTML_FAILCASE = """
Vue.component('fail_case', {
    template:
    `
    <div class="fail_case">
        <a-collapse accordion>
            <a-collapse-panel v-for="fail in fail_case" :key="fail.name" :header="fail.name">
                <a-collapse accordion>
                    <a-collapse-panel  v-for="(case_obj, idx) in fail.children" :header="'用例编号：' + case_obj.case_num" :key="idx">
                        <a-descriptions bordered >
                            <a-descriptions-item label="备注" :span="2">
                                <span style="font-size: 10px">{{case_obj.remark}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="运行结果">
                                <template v-if="case_obj.res === '成功'">
                                    <a-badge status="success" />
                                </template>
                                <template v-else>
                                    <a-badge status="error" />
                                </template>
                                <span style="font-size: 10px">{{case_obj.res}}</span>
                                
                            </a-descriptions-item>
                            <a-descriptions-item label="用例类型">
                                <span style="font-size: 10px">{{case_obj.type}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="失败中断">
                                <span style="font-size: 10px">{{case_obj.fail_break}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="元素" :span="2">
                                <span style="font-size: 10px">{{case_obj.el}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="查找方式">
                                <span style="font-size: 10px">{{case_obj.method}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="元素下标">
                                <span style="font-size: 10px">{{case_obj.index}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="操作对象">
                                <span style="font-size: 10px">{{case_obj.obj}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="操作方式">
                                <span style="font-size: 10px">{{case_obj.action}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="当前context">
                                <span style="font-size: 10px">{{case_obj.context}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="当前所有context">
                                <span style="font-size: 10px">{{case_obj.contexts}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="坐标轴">
                                <span style="font-size: 10px">{{case_obj.x1}},{{case_obj.y1}},{{case_obj.x2}},{{case_obj.y2}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="等待时间（实际）(s)">
                                <span style="font-size: 10px">{{case_obj.sleep_res}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="设定最大等待时间(s)">
                                <span style="font-size: 10px">{{case_obj.max_sleep}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="预期结果">
                                <span style="font-size: 10px">{{case_obj.hope}}</span>
                            </a-descriptions-item>
                            <a-descriptions-item label="报错信息" :span="2">
                                <span style="font-size: 10px">{{case_obj.error}}</span>
                            </a-descriptions-item>

                        </a-descriptions>
                    </a-collapse-panel>
                </a-collapse>
            </a-collapse-panel>
        </a-collapse>
    </div>
    `,
    data(){
        return{
            fail_case: %s
        }
    }
})
"""

HTML_END = """
var app = new Vue({
    el: '#app',
    template:
    `
    <div class="content">
        <div class="content-left">
            <h2 class="module">测试概览</h2>
            <div style="display: flex; flex-wrap: nowrap;">
                <test_overview/>
                <sta/>
            </div>

            <h2 class="module">失败用例详情</h2>
            <fail_case/>
        </div>
        <device_info/>
    </div>
    `,
})
</script>
</body>
"""


class GenerateHtmlReport():
    def __init__(self, simple, fail_case):
        self.simple = simple
        self.fail_case = fail_case

        self.fail_case['sta_data'][0]['rate'] = int(round(self.fail_case['sta_data'][0]['value'] / self.simple['fail'], 2) * 100)
        self.fail_case['sta_data'][1]['rate'] = int(round(self.fail_case['sta_data'][1]['value'] / self.simple['fail'], 2) * 100)
        self.fail_case['sta_data'][2]['rate'] = int(round(self.fail_case['sta_data'][2]['value'] / self.simple['fail'], 2) * 100)
        self.fail_case['sta_data'][3]['rate'] = int(round(self.fail_case['sta_data'][3]['value'] / self.simple['fail'], 2) * 100)
        self.fail_case['sta_data'][4]['rate'] = int(round(self.fail_case['sta_data'][4]['value'] / self.simple['fail'], 2) * 100)

    def gen_pass_rate(self):
        if self.simple['success'] == 0:
            return 0
        else:
            return round(
                (self.simple['success'] / self.simple['case_count']) * 100,
                1
            )

    def gen_title(self):
        return HTML_TITLE.format(project=self.simple['project'])

    def gen_overview(self):
        return HTML_OVERVIEW% dict(
           case_count=self.simple['case_count'],
           success=self.simple['success'],
           fail=self.simple['fail'],
           pass_rate=self.gen_pass_rate(),
           start_time=self.simple['start_time'],
           exec_time=self.simple['exec_time'],
        )

    def gen_device(self):
        return HTML_DEVICE % dict(
            platform=self.simple['platform'],
            version=self.simple['version'],
            device_name=self.simple['device_name']
        )

    def gen_sta(self):
        return HTML_STA1 + HTML_STA2 % self.simple['case_count'] + HTML_STA3 + HTML_STA4 % str(self.fail_case['sta_data']) + HTML_STA5

    def gen_fail_case(self):
        return HTML_FAILCASE % str(self.fail_case['fail_case'])

    def gen_report(self):
        html_txt = HTML_START + \
        self.gen_title() + \
        self.gen_overview() + \
        self.gen_device() + \
        self.gen_sta() + \
        self.gen_fail_case() + \
        HTML_END

        today = datetime.now().strftime('%Y-%m-%d')
        path = get_path('report/%s' % today)

        if not os.path.exists(path): os.mkdir(path)
        
        html_path = path + '/' + self.simple['project'] + '.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_txt)

        return html_path