HTML_TEMP = """
<!DOCTYPE html>
<head>
<meta charset="utf-8"/>
</head>

<body>
    <h3>
        <img style="margin-left: 25px; " src="http://172.16.7.217:8088/wisedu/test_platform/logo_img" alt="wisedu"/>
        <span style="font-weight: 600; font-size: 18px; vertical-align: super;">Mobile UI 自动化测试报告</span>
    </h3>
    <div style="height: 50px;
    background-color: #f7f7f7;
    border-top: 1px solid #DCDCDC;
    border-bottom: 1px solid #DCDCDC;">
        <span class="title" style="margin-left: 25px; font-weight: 600;
        font-size: 16px;
        line-height: 50px;">项目名称：</span>
        <span style="font-weight: 600;
        font-size: 16px;
        line-height: 50px;" >{project}</span>
    </div>

    <div style="margin: 0px 25px 20px; ">
        <p style="font-style: italic; font-size: 14px; color: #666">
            Mobile UI自动化测试报告如下，该报告由Mobile UI 自动化测试框架生成。
        </p>
        <p style="font-style: italic; font-size: 14px; color: #666">
            框架使用问题请联系@吴坤，以下为总览，详情请通过谷歌浏览器打开附件查看
        </p>
        <h2 style="color: #607d8b;">测试概览</h2>
        <div style="background-color: #f6f6f6;
        box-sizing: border-box;
        width: 600px;
        border: 1px solid #ddd;
        border-radius: 3px;
        padding: 10px;">
        <ul style="margin-top: 0px;margin-bottom: 0px;margin-left: 5px;padding-left: 10px;">
            <li style="font-size: 15px;line-height: 1.6;">
                <span style="color: #660;">测试用例:</span>
                <span style="color: #607d8b;">{case_count} 条</span>
            </li>
            <li style="font-size: 15px;line-height: 1.6;">
                <span style="color: #660;">通过率:</span>
                <span style="color: #CDAD00;">{pass_rate}%</span>
            </li>
            <li style="font-size: 15px;line-height: 1.6;">
                <span style="color: #660;">成功/失败:</span>
                <span style="color: #00CD66;">{success}</span>/<span style="color: red;">{fail}</span>
            </li>
            <li style="font-size: 15px;line-height: 1.6;">
                <span style="color: #660;">开始时间:</span>
                <span style="color: #607d8b;">{start_time}</span>
            </li>
            <li style="font-size: 15px;line-height: 1.6;">
                <span style="color: #660;">总耗时:</span>
                <span style="color: #607d8b;">{exec_time} s</span>
            </li>
        </ul>
        </div>
            
        <h2 style="color: #607d8b;">设备信息</h2>
        <div style="background-color: #f6f6f6;
            width: 600px;
            box-sizing: border-box;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 10px;">
            <ul style="margin-top: 0px;margin-bottom: 0px;margin-left: 5px;padding-left: 10px;">
                <li style="font-size: 15px;line-height: 1.6;">
                    <span style="color: #660;">操作系统:</span>
                    <span style="color: #607d8b;">{platform}</span>
                </li>
                <li style="font-size: 15px;line-height: 1.6;">
                    <span style="color: #660;">系统版本:</span>
                    <span style="color: #607d8b;">{version}</span>
                </li>
                <li style="font-size: 15px;line-height: 1.6;">
                    <span style="color: #660;">设备名称:</span>
                    <span style="color: #607d8b;">{device_name}</span>
                </li>

            </ul>
        </div>

        <h2 style="color: #607d8b;">失败用例</h2>
        <table style="width: 600px; border-collapse: collapse;">
            <thead>
                <tr style="background-color: #f8f8f8;">
                    <th style="text-align: left; width: 70%;
                    padding: 6px 13px;
                    border: 1px solid #ddd;
                    font-size: 14px;">用例名称</th>
                    <th style="text-align: left; width: 20%;
                    padding: 6px 13px;
                    border: 1px solid #ddd;
                    font-size: 14px;">报错类型</th>
                    <th style="text-align: left;
                    padding: 6px 13px;
                    border: 1px solid #ddd;
                    font-size: 14px;">结果</th>
                </tr>
            </thead>
            <tbody>
                {fail_case}
            </tbody>
        </table>
        <h2 style="color: #607d8b;">所有用例</h2>
        <table style="width: 600px; border-collapse: collapse;">
            <thead>
                <tr style="background-color: #f8f8f8;">
                    <th style="text-align: left; width: 70%;
                    padding: 6px 13px;
                    border: 1px solid #ddd;
                    font-size: 14px;">用例名称</th>
                    <th style="text-align: left; width: 20%;
                    padding: 6px 13px;
                    border: 1px solid #ddd;
                    font-size: 14px;">报错类型</th>
                    <th style="text-align: left;
                    padding: 6px 13px;
                    border: 1px solid #ddd;
                    font-size: 14px;">结果</th>
                </tr>
            </thead>
            <tbody>
                {all_case}
            </tbody>
        </table>
    </div>
</body>
"""


class GenerateSimpleReport():
    def __init__(self, project, case_count, success, fail, start_time, exec_time,
                 platform, version, device_name, fail_case, all_case):
        self.project = project
        self.case_count = case_count
        self.success = success
        self.fail = fail
        self.start_time = start_time
        self.exec_time = exec_time
        self.platform = platform
        self.version = version
        self.device_name = device_name
        self.fail_case = fail_case
        self.all_case = all_case

    def gen_pass_rate(self):
        if self.success == 0:
            return 0
        else:
            return round(
                (self.success / self.case_count) * 100,
                1
            )

    def gen_case_text(self, case_list):
        temp = """
         <tr>
                    <td style="text-align: left;
        padding: 6px 13px;
        border: 1px solid #ddd;
        font-size: 14px;">
                        {case_name}
                    </td>
                    <td style="text-align: left;
        padding: 6px 13px;
        border: 1px solid #ddd;
        font-size: 14px;">
                        {fail_type}
                    </td>
                    <td style="text-align: left;
        padding: 6px 13px;
        border: 1px solid #ddd;
        font-size: 14px;
        color: {color};">
                        {res}
                    </td>
                </tr>
        """
        case_text = ''

        for case in case_list:
            if case[1]:
                color = '#00CD66'
                res = '成功'
            else:
                color = 'red'
                res = '失败'
            case_text += temp.format(
                case_name=case[0],
                fail_type=case[2],
                color=color,
                res=res
            )
        return case_text

    def gen_report(self):
        return HTML_TEMP.format(
            project=self.project,
            case_count=self.case_count,
            success=self.success,
            fail=self.fail,
            pass_rate=self.gen_pass_rate(),
            start_time=self.start_time,
            exec_time=self.exec_time,
            platform=self.platform,
            version=self.version,
            device_name=self.device_name,
            fail_case=self.gen_case_text(self.fail_case),
            all_case=self.gen_case_text(self.all_case),
        )
