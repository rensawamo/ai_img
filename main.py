from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

import streamlit as st

KEY = st.secrets.AzureApiKey.key
ENDPOINT = st.secrets.AzureApiKey.endpoint

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(your_filepath):

    local_image = open(your_filepath, "rb")
    tags_result = computervision_client.tag_image_in_stream(local_image)

    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name

def detect_objects(f_path):

    local_image = open(f_path, "rb")
    detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results_local.objects
    return objects

from PIL import ImageDraw
from PIL import ImageFont

import streamlit as st
st.title('AI物体認識アプリ')

uploaded_file = st.file_uploader('画像選択', type=['jpg', 'png'])

if uploaded_file is not None:
    st.markdown('以下が検出されました')
    img = Image.open(uploaded_file)
    img_path = f'imerge/{uploaded_file.name}'

    img.save(img_path)

    objects = detect_objects(img_path)

    
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        
        caption = object.object_property
        font = ImageFont.truetype(font='./Calypso.ttf', size=40)
        text_w, text_h = draw.textsize(caption, font=font)

        draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline='blue', width=5)
        draw.rectangle([(x, y), (x+text_w, y+text_h)], fill="blue")
        draw.text((x,y), caption, fill="white", font=font)


    st.image(img)
   