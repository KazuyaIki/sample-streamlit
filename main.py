import streamlit as st
from PIL import Image, ImageDraw
import requests
import json
import io

st.title('顔認識アプリ')

subscription_key = '22ac5e1208ac4bf7be0a4eb1ea17eb72'
assert subscription_key
face_api_url = 'https://20201129kiki.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("Choose an image ...", type='jpg')

# if uploaded_file is not None:
if uploaded_file:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリを取得
    
    headers = {'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }

    response = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
    results = response.json()
    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline='green', width=2)
    st.image(img, caption="uploaded image", use_column_width=False)

