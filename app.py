from flask import render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import requests
import json
import time
import uuid
from datetime import datetime
import boto3
from dotenv import load_dotenv
from app.services.code_service import CodeService
from app import app

# 加载环境变量
load_dotenv()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
def generate():
    data = request.get_json()
    activation_code = data.get('activation_code')
    image_urls = data.get('image_urls', [])
    prompt = data.get('prompt', '')

    if not activation_code:
        return jsonify({'error': '请输入激活码'}), 400

    # 验证激活码
    is_valid, error_message, code_record = CodeService.validate_code(activation_code)
    if not is_valid:
        return jsonify({'error': error_message}), 400

    try:
        # 标记激活码为使用中
        CodeService.mark_code_as_using(code_record)

        # 图片生成逻辑
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
        response_data = response.json()

        # 检查生成是否失败
        if 'choices' in response_data and response_data['choices']:
            message_content = response_data['choices'][0]['message']['content']
            if '生成失败' in message_content or 'is_output_rejection' in message_content:
                CodeService.reset_code_status(code_record)
                return jsonify({
                    'error': '图片生成失败，请修改提示词后重试',
                    'details': message_content
                }), 400

        # 生成成功，标记激活码为已使用
        CodeService.mark_code_as_used(code_record)
        return jsonify(response_data)

    except Exception as e:
        # 发生错误时重置状态
        CodeService.reset_code_status(code_record)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
