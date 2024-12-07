from flask import Flask, render_template, request

app = Flask(__name__)

# 单位转换（字节，字节数为基础）
data_size_units = {
    'TB': 1024 ** 4,  # 1 TB = 1024^4 字节
    'GB': 1024 ** 3,  # 1 GB = 1024^3 字节
    'MB': 1024 ** 2,  # 1 MB = 1024^2 字节
    'KB': 1024,  # 1 KB = 1024 字节
    'B': 1  # 1 字节
}

# 带宽单位转换（比特数为基础）
bandwidth_units = {
    'TBps': 8 * 1024 ** 4,  # 1 TBps = 8 * 1024^4 比特
    'GBps': 8 * 1024 ** 3,  # 1 GBps = 8 * 1024^3 比特
    'Mbps': 10 ** 6,  # 1 Mbps = 10^6 比特
    'kbps': 10 ** 3,  # 1 kbps = 10^3 比特
    'bps': 1  # 1 bps = 1 比特
}


def calculate_transfer_time(data_size, data_unit, bandwidth, bandwidth_unit):
    """
    计算数据传输时间
    :param data_size: 数据量
    :param data_unit: 数据量单位
    :param bandwidth: 带宽
    :param bandwidth_unit: 带宽单位
    :return: 传输时间（单位：秒）
    """
    # 转换数据量为字节
    data_size_bytes = data_size * data_size_units[data_unit]

    # 转换带宽为比特每秒
    bandwidth_bits = bandwidth * bandwidth_units[bandwidth_unit]

    # 计算传输时间（单位：秒）
    transfer_time = data_size_bytes * 8 / bandwidth_bits  # 因为带宽是比特单位，数据量是字节，所以乘以8

    return transfer_time


def format_time(seconds):
    """
    将秒数转换为 天、小时、分钟、秒 的格式
    :param seconds: 总秒数
    :return: 格式化后的时间字符串
    """
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{int(days)} 天 {int(hours)} 小时 {int(minutes)} 分钟 {int(secs)} 秒"


@app.route('/', methods=['GET', 'POST'])
def index():
    data_size = None
    data_unit = 'TB'
    bandwidth = None
    bandwidth_unit = 'Mbps'
    transfer_time = None
    error = None

    if request.method == 'POST':
        try:
            # 获取前端表单数据
            data_size = float(request.form['data_size'])
            data_unit = request.form['data_unit']
            bandwidth = float(request.form['bandwidth'])
            bandwidth_unit = request.form['bandwidth_unit']

            if data_size <= 0 or bandwidth <= 0:
                error = "数据量和带宽必须为正数！"
            else:
                # 计算传输时间（秒）
                transfer_time_seconds = calculate_transfer_time(data_size, data_unit, bandwidth, bandwidth_unit)

                # 格式化传输时间
                transfer_time = format_time(transfer_time_seconds)
        except ValueError:
            error = "请输入有效的数字！"

    return render_template('index.html', data_size=data_size, data_unit=data_unit, bandwidth=bandwidth,
                           bandwidth_unit=bandwidth_unit, transfer_time=transfer_time, error=error)


if __name__ == '__main__':
    app.run(debug=True)
