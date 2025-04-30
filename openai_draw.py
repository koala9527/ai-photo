import requests
import json

url = "https://yunwu.ai/v1/chat/completions"

payload = json.dumps({
   "model": "gpt-4o-image-vip",
   "messages": [
      {
         "role": "system",
         "content": "You are a helpful assistant."
      },
      {
         "role": "user",
         "content": [
            {
               "type": "text",
               "text": "请画一张极其平凡无奇的iPhone 自拍照，没有明确的主体或构图感，就像是随手一拍的快照。照片略带运动模糊，阳光或店内灯光不均导致轻微曝光过度。角度尴尬、构图混乱，整体呈现出一种刻意的平庸感-就像是从口袋里拿手机时不小心拍到的一张自拍。主角是我上传的两张图，晚上，旁边是香港会展中心，在香港维多利亚港旁边。"
            },
            {
               "type": "image_url",
               "image_url": {
                  "url": "https://hatui.s3.bitiful.net/test%2Fliudehua.png?no-wait=on"
               }
            },
            {
               "type": "image_url",
               "image_url": {
                  "url": "https://hatui.s3.bitiful.net/test%2Fyangmi.png?no-wait=on"
               }
            }
         ]
      }
   ]
})
headers = {
   'Accept': 'application/json',
   'Content-Type': 'application/json',
   'Authorization': 'Bearer sk-qiV1cYzY2e9YWrGUcVw80uoWScM6cqUULCsx8D9WFPaZhQ8t'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)