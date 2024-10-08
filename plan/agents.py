import os
import dspy
from dotenv import load_dotenv
from dspy import InputField, OutputField, Signature, Module

load_dotenv()

lm = dspy.OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), max_tokens=4096)
dspy.settings.configure(lm=lm)

class Json2NL(Signature):
    """
    Convert raster image coordinates and object classes in JSON to a natural language description.
    ---
    Input: 
    - Raster JSON data with object classes, coordinates, and confidence scores.
    
    Output:
    - Natural language description based on the raster JSON.
    """

    json_data = InputField(desc="JSON object containing object coordinates, classes, and confidence scores.")
    natural_language_description = OutputField(desc="Natural language description of the raster data.")

