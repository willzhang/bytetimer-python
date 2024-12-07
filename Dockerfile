# 使用官方的 Python 3 镜像作为基础镜像
FROM python:3.13.1-slim

# 设置工作目录
WORKDIR /app

# 复制本地代码到容器内的工作目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 开放容器的 5000 端口，Flask 默认运行在 5000 端口
EXPOSE 5000

# 设置 Flask 环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 启动 Flask 应用
CMD ["flask", "run"]
