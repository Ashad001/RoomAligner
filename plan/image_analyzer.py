import base64
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class ImageAnalyzer:
    def __init__(self, model_name="llama-3.2-90b-vision-preview"):
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
                        "text": f"""You are a Vision Language Model tasked with analyzing room images. Your primary focus is to extract visual features such as furniture arrangement, room layout, and suggestions for optimizing space or improving aesthetics.

                        Your response should be structured as follows:

                        1. Room Layout Description: Describe the layout of the room, including major structural elements (e.g., walls, windows, doors).
                        
                        2. Furniture Analysis: Identify and describe the furniture in the room, including positioning, type of furniture, and any functional zones (e.g., seating area, work area).

                        3. Suggestions for Improvement: Provide actionable suggestions for optimizing the room layout, improving space usage, or enhancing the aesthetics. Focus on furniture arrangement, lighting, and potential decor adjustments.
                        """
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
