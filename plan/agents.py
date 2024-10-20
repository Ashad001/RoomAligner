import os
import dspy
from dotenv import load_dotenv
from dspy import InputField, OutputField, Signature, Module
from typing import List, Dict, Any

load_dotenv(".env")
lm = dspy.GROQ(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"), max_tokens=4096)
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
    You are tasked with analyzing room layouts and furniture arrangements from visual data. Your objective is to create a professional and detailed interior design report based on the provided analysis. This report should include the following sections:

    1. Room Layout Description: Begin with a thorough overview of the room's structural elements, including walls, windows, and doors. Clearly outline how these features impact the overall design and flow of the space.

    2. Furniture Analysis: Identify and describe the types of furniture present in the room, detailing their arrangements and the purpose of each area (e.g., seating areas, workspaces, and decorative zones). Emphasize any key aspects that enhance the room's functionality.

    3. Suggestions for Improvement: Provide actionable recommendations for optimizing the room's layout, enhancing aesthetics, and improving functionality. Discuss potential adjustments to the arrangement of furniture, suggest new decor ideas, and consider possible changes to lighting.

    Ensure that your output is structured, well-organized, and presented in a clear and professional manner to facilitate understanding and usability for clients seeking design guidance.
    """

    input_structure = InputField(type=str, desc="Raw room analysis from visual data, encompassing layout, furniture details, and suggestions for improvement.")
    space_optimized_structure = OutputField(type=str, desc="A polished, professional report that organizes the room analysis into clearly defined sections: room layout description, furniture analysis, and actionable optimization suggestions.")


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