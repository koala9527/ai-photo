FROM docker.io/library/python:3.11

WORKDIR /app

# 复制项目文件
COPY requirements.txt .

# 使用阿里云 PyPI 镜像
RUN pip install -r requirements.txt

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