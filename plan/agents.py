import os
import dspy
from dotenv import load_dotenv
from dspy import InputField, OutputField, Signature, Module
from typing import List, Dict, Any

load_dotenv(".env")
lm = dspy.OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), max_tokens=4096)
dspy.settings.configure(lm=lm)

class Json2NL(Signature):
    """
    Convert raster image coordinates and object classes in JSON to a detailed natural language description.
    ---
    Input: 
    - Raster JSON data with object classes, coordinates, and confidence scores.
    
    Output:
    - Natural language description based on the raster JSON.
    """

    data = InputField(type=str, desc="Data containing object coordinates, classes, and confidence scores.")
    natural_language_description = OutputField(type=str, desc="Natural language description of the input data.")
    

class InteriorDesigner(Signature):
    """ 
    You are a professional interior designer focusing on space utilization optimization. 
    Based on the current room structure provided, you will suggest how the user can utilize free space more effectively, rearrange furniture for better flow, and suggest any additional storage or organizational solutions.
    ---
    Input: Current Room Structure
    Output: Suggested Room Structure with focus on space optimization
    """
    input_structure = InputField(type=str, desc="Current room structure with furniture and object details.")
    space_optimized_structure = OutputField(type=str, desc="Suggested room structure with recommendations for optimizing space usage and flow.")


class GeneratePlan(Module):
    def __init__(self):
        super().__init__()
        self.j2nl = dspy.ChainOfThought(Json2NL)
        
    def forward(self, data):
        """
        Generate natural language suggestions based on the raster data.
        """
        print(data)
        nl_description = self.j2nl(data=data)
        return nl_description.natural_language_description
        
class GenerateSuggestions(Module):
    def __init__(self):
        super().__init__()
        self.id = dspy.ChainOfThought(InteriorDesigner)
        
    def forward(self, input_structure):
        """
        Generate suggestions for room structure based on the input room structure.
        """
        suggested_structure = self.id(input_structure=input_structure)
        return suggested_structure.space_optimized_structure