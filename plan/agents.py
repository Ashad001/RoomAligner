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
    

class InteriorDesigner(Signature):
    """ 
    You are a professional interior designer and you have been asked to design a room based on user's current room plan.
    You can suggest how the user can utilize free space in the room and what furniture can be added to make the room look better.
    ---
    Input: Current Room Structure
    Output: Suggested Room Structure
    """
    input_structure = InputField(desc="Current room structure.")
    suggested_structure = OutputField(desc="Suggested room structure.")

class GeneratePlan(Module):
    def __init__(self):
        super().__init__()
        self.j2nl = dspy.ChainOfThought(Json2NL)
        
    def forward(self, json_data):
        """
        Generate natural language suggestions based on the raster data.
        """
        nl_description = self.j2nl(json_data)
        return nl_description.natural_language_description
        
class GenerateSuggestions(Module):
    def __init__(self):
        super().__init__()
        self.id = dspy.ChainOfThought(InteriorDesigner)
        
    def forward(self, input_structure):
        """
        Generate suggestions for room structure based on the input room structure.
        """
        suggested_structure = self.id(input_structure)
        return suggested_structure.suggested_structure