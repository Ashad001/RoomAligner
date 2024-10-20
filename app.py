import os
import base64
import json
import requests
from io import BytesIO
from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from plan.agents import GeneratePlan, GenerateSuggestions
from plan.image_analyzer import ImageAnalyzer
from raster.raster import InferenceClient
from utils.preprocess_data import preprocess_data
from PIL import Image

load_dotenv()

app = FastAPI(title="Interior Designer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# required classes
inference_client = InferenceClient()
plan_generator = GeneratePlan()
image_analyzer = ImageAnalyzer()
suggestions_generator = GenerateSuggestions()

@app.post("/upload-room-image/")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload room image and get natural language description and suggested room layout.
    Supports multiple image formats like PNG, JPEG, BMP.
    """
    return await process_image(file.file)


@app.post("/upload-room-image-url/")
async def upload_image_url(image_url: str = Form(...)):
    """
    Upload room image from URL and get natural language description and suggested room layout.
    """
    try:
        # Fetch the image from the URL
        response = requests.get(image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Image could not be retrieved from the URL.")
        
        img = Image.open(BytesIO(response.content))
        image_format = img.format  # Identify the image format (e.g., JPEG, PNG)

        if image_format not in ["JPEG", "PNG", "BMP"]:
            raise HTTPException(status_code=400, detail="Unsupported image format. Please upload a JPEG, PNG, or BMP image.")

        buffered = BytesIO()
        img.save(buffered, format=image_format)  # Keep the original format
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Process the image as before (e.g., object classification, room structure analysis)
        room_structure = image_analyzer.generate_floor_plan_details(image_base64, "")
        formatted_room_structure = suggestions_generator.forward(room_structure.content)

        return JSONResponse(content={
            "natural_language_description": "i excluded this for now",
            "room_structure": room_structure.content,
            "formatted_room_structure": formatted_room_structure
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

async def process_image(img):
    """
    Common image processing logic to handle both file upload and image URL.
    """
    try:
        image_format = img.format  # Identify the image format (e.g., JPEG, PNG)

        if image_format not in ["JPEG", "PNG", "BMP"]:
            raise HTTPException(status_code=400, detail="Unsupported image format. Please upload a JPEG, PNG, or BMP image.")

        buffered = BytesIO()
        img.save(buffered, format=image_format)  # Keep the original format
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Step 1: Classify objects in the image (commented out for now)
        # result = inference_client.infer_image(image_base64)
        # data = preprocess_data(result)

        # Step 2: Generate a natural language description (excluded for now)
        # nl_description = plan_generator.forward(data)

        # Step 3: Analyze room structure and generate suggestions
        room_structure = image_analyzer.generate_floor_plan_details(image_base64, "")
        formatted_room_structure = suggestions_generator.forward(room_structure.content)

        # Return response as JSON
        return JSONResponse(content={
            "natural_language_description": "i excluded this for now",  # nl_description
            "room_structure": room_structure.content,
            "formatted_room_structure": formatted_room_structure
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Interior Designer API!"}
