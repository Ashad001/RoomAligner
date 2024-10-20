import os
import json
from dotenv import load_dotenv
from plan.agents import GeneratePlan, GenerateSuggestions
from plan.image_analyzer import ImageAnalyzer
# from raster.raster import InferenceClient
from utils.preprocess_data import preprocess_data
import streamlit as st
import base64
from io import BytesIO
from PIL import Image

load_dotenv()

st.set_page_config(page_title="Interior Designer", layout="wide")

st.title("🧑🏼 Interior Design Assistant")

# inference_client = InferenceClient()
plan_generator = GeneratePlan()
image_analyzer = ImageAnalyzer()
suggestions_generator = GenerateSuggestions()

st.write("Welcome to the Interior Design Assistant!")
st.write("Please upload an image of your room plan.")

# Allowing multiple image formats
image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "tiff"])
if image is not None:
    img = Image.open(image)
    st.image(img, caption="Uploaded Image.", use_column_width=True)

    # Get the image format
    image_format = img.format if img.format else "JPEG"
    
    # Convert the image to base64
    buffered = BytesIO()
    img.save(buffered, format=image_format)
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # st.write("Classifying the objects in the image...")
    # result = inference_client.infer_image(image_base64)  
    # data = preprocess_data(result)

    # st.write("Objects in the image have been classified.")
    # st.write("Generating a natural language description based on the image...")

    # nl_description = plan_generator.forward("")
    # st.write("Natural language description:")
    # st.write(nl_description)

    st.write("Generating suggestions for room structure based on the image...")
    room_structure = image_analyzer.generate_floor_plan_details(image_base64, "")  
    st.write("Current room structure:")
    st.write(room_structure.content)
    
    suggested_structure = suggestions_generator.forward(room_structure.content)
    
    st.write("Suggested room structure:")
    st.write(suggested_structure)
