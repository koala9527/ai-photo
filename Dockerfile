<<<<<<< HEAD
#
FROM docker.io/library/python:3.11


WORKDIR /app

=======
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python

WORKDIR /app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

>>>>>>> 5112722f486a450fef2f6fc31a4aeba4303754f0
# 复制项目文件
COPY requirements.txt .

# 使用阿里云 PyPI 镜像
<<<<<<< HEAD
RUN pip install -r requirements.txt
=======
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt
>>>>>>> 5112722f486a450fef2f6fc31a4aeba4303754f0

# 复制其余项目文件
COPY . .

# 创建上传目录
RUN mkdir -p static/uploads

# 设置环境变量
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"] 