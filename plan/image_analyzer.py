import base64
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class ImageAnalyzer:
    def __init__(self, model_name="llava-v1.5-7b-4096-preview"):
        self.model_name = model_name
        self.client = Groq()

    def encode_image(self, image_path):
        """
        Encodes the image from the given file path into base64 format.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def generate_floor_plan_details(self, image_base64, coordinates_message, temperature=1, max_tokens=1024, top_p=1):
        image_url = f"data:image/jpeg;base64,{image_base64}"
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant specialized in analyzing floor plan images to provide a comprehensive, room-by-room analysis. For each room in the image, you will identify its structure, the positioning of furniture, and functional zones. Your task is to analyze every room individually, using visual cues from the image to identify specific objects such as beds, sofas, tables, and other furniture or fixtures. Evaluate how space is used within each room, and describe any potential areas for optimizing furniture arrangement or improving space utilization."

                    },
                    {
                        "type": "text",
                        "text": coordinates_message
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
            stop=None
        )

        return completion.choices[0].message

if __name__ == "__main__":
    # Initialize the ImageAnalyzer with a sample image
    analyzer = ImageAnalyzer()
    
    # Encode the image (assumed to be located at the specified path)
    encoded_image = analyzer.encode_image("./raster_images/1.jpg")
    
    # Provide a detailed floor plan analysis with image and coordinates message
    floor_plan_details = analyzer.generate_floor_plan_details(
        encoded_image,
        "The room has a coffee table at coordinates (684, 95), a large sofa at (574, 580), and a bed at (457, 177). Please describe the room's layout, furniture positions, and identify other key elements in the image."
    )
    
    # Print the detailed description of the floor plan
    print(floor_plan_details)
