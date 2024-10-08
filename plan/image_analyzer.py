import base64
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

class ImageAnalyzer:
    def __init__(self, image_path, model_name="llama-3.2-11b-vision-preview"):
        self.image_path = image_path
        self.model_name = model_name
        self.client = Groq()

    def encode_image(self):
        """
        Encodes the image from the given file path into base64 format.
        """
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def generate_suggestions(self, coordinates_message, temperature=1, max_tokens=1024, top_p=1):
        """
        Generates interior design suggestions based on the image and provided coordinates.
        """
        image_base64 = self.encode_image()
        image_url = f"data:image/jpeg;base64,{image_base64}"
        
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant designed to analyze floor plan images and corresponding object coordinates (like furniture, sinks, and beds). Your task is to provide suggestions for interior design improvements based on the layout provided, taking into consideration space optimization, furniture placement, and functional areas. You should generate detailed, professional, and personalized suggestions, addressing both aesthetics and practicality. Additionally, if necessary, you can suggest adding, removing, or rearranging furniture items to optimize the use of space. When the user provides coordinates in natural language, interpret the coordinates to identify objects in the space and provide tailored recommendations. Be prepared to explain why certain changes are beneficial."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
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
    analyzer = ImageAnalyzer("./raster_images/1.jpg")
    suggestion_message = analyzer.generate_suggestions(
        "I have a room with a coffee table at coordinates (684, 95), a large sofa at (574, 580), and a bed at (457, 177). Can you suggest how I can rearrange the furniture for better space utilization and suggest any additional furniture I should consider?"
    )
    print(suggestion_message)
