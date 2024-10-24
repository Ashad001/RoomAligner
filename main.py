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

st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
            font-family: "Arial", sans-serif;
        }
        .stButton > button {
            color: white;
            background-color: #007bff;
            border-radius: 4px;
            padding: 8px 16px;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("🧑🏼 Interior Design Assistant")

st.markdown("""
    Welcome to the **Interior Design Assistant**! 
    Upload an image of your room plan and receive design suggestions and structure recommendations.
    """)

st.sidebar.header("Upload Section")
st.sidebar.write("Please upload an image of your room plan:")

image = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "tiff"])

if image:
    img = Image.open(image)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    image_format = img.format if img.format else "JPEG"
    buffered = BytesIO()
    img.save(buffered, format=image_format)
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    if st.button("Analyze Image"):
        st.write("Generating room structure details...")

        plan_generator = GeneratePlan()
        image_analyzer = ImageAnalyzer()
        suggestions_generator = GenerateSuggestions()

        room_structure = image_analyzer.generate_floor_plan_details(image_base64, "")
        st.subheader("Current Room Structure")
        st.write(room_structure.content)

        st.write("Generating design suggestions...")
        suggested_structure = suggestions_generator.forward(room_structure.content)

        st.subheader("Suggested Room Structure")
        st.write(suggested_structure)

else:
    st.sidebar.write("No image uploaded yet.")

st.sidebar.write("Click 'Analyze Image' to generate room suggestions.")
