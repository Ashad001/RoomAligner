import os
import json
from dotenv import load_dotenv
from plan.agents import GeneratePlan, GenerateSuggestions
from plan.image_analyzer import ImageAnalyzer
from raster.raster import InferenceClient
import streamlit as st

load_dotenv()

st.title("Interior Design Assistant")

def main():
    st.write("Welcome to the Interior Design Assistant!")
    st.write("Please upload an image of your room plan.")
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        st.write("")
        st.write("Classifying the objects in the image...")
        inference_client = InferenceClient()
        result = inference_client.infer_image(uploaded_file)
        inference_client.save_results(result, "./json/results.json")
        st.write("Objects in the image have been classified.")
        st.write("Generating a natural language description based on the image...")
        with open("./json/results.json", "r") as f:
            json_data = json.load(f)
        plan_generator = GeneratePlan()
        nl_description = plan_generator(json_data)
        st.write("Natural language description:")
        st.write(nl_description)
        st.write("Generating suggestions for room structure based on the image...")
        image_analyzer = ImageAnalyzer()
        room_structure = image_analyzer(json_data)
        suggestions_generator = GenerateSuggestions()
        suggested_structure = suggestions_generator(room_structure)
        st.write("Suggested room structure:")
        st.write(suggested_structure)
        

if __name__=="__main__":
    main()