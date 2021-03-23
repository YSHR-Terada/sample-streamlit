import streamlit as st
import requests
import io
from PIL import Image
from PIL import ImageDraw

st.title('顔認識アプリ')

SUBSCRIPTION_KEY = 'b94438af04374b428b9f615c8275cabb'
face_api_url = 'https://20210321terada.cognitiveservices.azure.com/face/v1.0/detect'
img_file_nm = 'sample_06.jpg'
assert SUBSCRIPTION_KEY

headers = {
    'Content-Type':'application/octet-stream',
    'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
}
params = {
    'returnFaceId': 'true',
    'returnFaceAttributes': 'blur,exposure,noise,age,gender,facialhair,glasses,hair,makeup,accessories,occlusion,headpose,emotion,smile'
}


uploaded_file = st.file_uploader("Choose an image...",type='jpg')
if uploaded_file is not None:
  img = Image.open(uploaded_file)
  with io.BytesIO() as output:
      img.save(output,format="JPEG")
      binary_img = output.getvalue()

  response = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
  results = response.json()

  for result in results:
      rect = result['faceRectangle']
      draw = ImageDraw.Draw(img)
      info_text = "gender:{0} age:{1}".format(result['faceAttributes']['gender'],result['faceAttributes']['age'])
      draw.text((rect['left'],rect['top']-10),info_text,fill=(255,0,0,128))
      draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['width'])],fill=None,outline='green',width=3)
  st.image(img,caption='Uploaded Image.',use_column_width=True)