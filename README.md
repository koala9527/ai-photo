# AI 图片合成服务

基于 Flask 和 OpenAI API 的 AI 图片合成服务，支持多图片上传和自定义提示词生成。

## 功能特点

- 支持多图片上传（最多4张）
- 自定义提示词输入
- 实时生成进度显示
- 图片预览和删除
- 生成结果展示和下载
- Docker 容器化部署
- S3 对象存储支持

## 技术栈

- 后端：Flask + Gunicorn
- 前端：HTML + Tailwind CSS
- 存储：S3 对象存储
- AI：OpenAI API
- 部署：Docker + Docker Compose

## 环境要求

- Python 3.9+
- Docker & Docker Compose
- S3 兼容的对象存储服务
- OpenAI API 访问权限

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd ai-draw
```

### 2. 配置环境变量

复制 `.env.example` 文件为 `.env`，并填写必要的配置信息：

```bash
cp .env.example .env
```

需要配置的环境变量：
- S3 配置（endpoint, region, access key, secret key, bucket）
- OpenAI API 配置（api key, api url）
- Flask 配置（环境变量等）

### 3. 开发环境运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py
```

### 4. Docker 部署

```bash
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 项目结构

```
.
├── app.py              # Flask 应用主文件
├── templates/          # HTML 模板
│   └── index.html     # 主页面
├── static/            # 静态文件
│   └── uploads/       # 临时上传目录
├── Dockerfile         # Docker 构建文件
├── docker-compose.yml # Docker Compose 配置
├── requirements.txt   # Python 依赖
├── .env              # 环境变量配置
└── README.md         # 项目说明文档
```

## API 接口

### 1. 上传图片

- 端点：`POST /upload`
- 参数：`images[]`（多文件）
- 返回：`{ "urls": ["url1", "url2", ...] }`

### 2. 生成图片

- 端点：`POST /generate`
- 参数：
  ```json
  {
    "image_urls": ["url1", "url2", ...],
    "prompt": "自定义提示词"
  }
  ```
- 返回：OpenAI API 响应

## 部署说明

### 生产环境配置

1. 确保 `.env` 文件配置正确
2. 使用 Docker Compose 部署：
   ```bash
   docker-compose up -d
   ```
3. 服务将在 `http://localhost:8109` 上运行

### 注意事项

- 确保 S3 存储桶已正确配置并具有适当的访问权限
- 生产环境中使用 HTTPS
- 定期备份重要数据
- 监控服务状态和资源使用情况

## 开发说明

### 本地开发

1. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行开发服务器：
   ```bash
   python app.py
   ```

### 代码规范

- 遵循 PEP 8 规范
- 使用类型注解
- 编写单元测试
- 保持代码简洁清晰

## 常见问题

1. 上传失败
   - 检查文件大小是否超过限制（16MB）
   - 确认文件格式是否支持
   - 验证 S3 配置是否正确

2. 生成失败
   - 检查 OpenAI API 密钥是否有效
   - 确认网络连接是否正常
   - 查看服务器日志获取详细错误信息

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。
