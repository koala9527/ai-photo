from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import requests
import json
import time
import uuid
from datetime import datetime
import boto3
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_path():
    # 生成日期路径和文件名
    now = datetime.now()
    date_path = now.strftime('%Y/%m/%d')
    filename = f"{now.strftime('%H%M%S')}_{uuid.uuid4().hex[:8]}"
    return date_path, filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'images[]' not in request.files:
        return jsonify({'error': '没有文件被上传'}), 400
    
    files = request.files.getlist('images[]')
    if len(files) > 4:
        return jsonify({'error': '最多只能上传4张图片'}), 400

    uploaded_urls = []
    for file in files:
        if file and allowed_file(file.filename):
            date_path, filename = get_file_path()
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            full_path = f"{date_path}/{filename}.{file_extension}"
            
            # 保存到本地
            local_path = os.path.join(app.config['UPLOAD_FOLDER'], full_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            file.save(local_path)
            
            # 上传到S3
            client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
                aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
                endpoint_url=os.getenv('S3_ENDPOINT'),
                region_name=os.getenv('S3_REGION')
            )
            
            try:
                client.upload_file(
                    local_path,
                    os.getenv('S3_BUCKET'),
                    full_path
                )
                # 生成可访问的URL
                url = f"{os.getenv('S3_ENDPOINT')}/{os.getenv('S3_BUCKET')}/{full_path}"
                uploaded_urls.append(url)
                
                # 删除本地文件
                os.remove(local_path)
            except Exception as e:
                print(f"上传到S3失败: {str(e)}")
                return jsonify({'error': '文件上传失败'}), 500

    return jsonify({'urls': uploaded_urls})

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    image_urls = data.get('image_urls', [])
    custom_prompt = data.get('prompt', '')
    
    # 默认提示词
    default_prompt = "请画一张极其平凡无奇的iPhone 自拍照，没有明确的主体或构图感，就像是随手一拍的快照。照片略带运动模糊，阳光或店内灯光不均导致轻微曝光过度。角度尴尬、构图混乱，整体呈现出一种刻意的平庸感-就像是从口袋里拿手机时不小心拍到的一张自拍。主角是陈奕迅和谢霆锋，晚上，旁边是香港会展中心，在香港维多利亚港旁边。"
    
    # 使用自定义提示词或默认提示词
    prompt = custom_prompt if custom_prompt else default_prompt
    
    # 如果没有上传图片，使用默认图片
    if not image_urls:
        image_urls = []

    messages = [
        {
            "type": "text",
            "text": prompt
        }
    ]
    
    for image_url in image_urls:
        messages.append({
            "type": "image_url",
            "image_url": {
                "url": image_url
            }
        })

    payload = json.dumps({
        "model": "gpt-4o-image-vip",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": messages
            }
        ]
    })
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    
    response = requests.post(os.getenv('OPENAI_API_URL'), headers=headers, data=payload)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
