import os
import json
from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv

load_dotenv()

class InferenceClient:
    def __init__(self, api_url = "https://detect.roboflow.com", api_key = os.getenv("ROBOFLOW_API_KEY")):
        self.client = InferenceHTTPClient(api_url=api_url, api_key=api_key)

    def infer_image(self, image_path: str, model_id: str = "robin-c75re/1"):
        return self.client.infer(image_path, model_id=model_id)

    def save_results(self, results, output_path):
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=4)

if __name__ == "__main__":
    image_path = "./raster_images/1.jpg"
    output_path = "./json/results.json"

    inference_client = InferenceClient()
    result = inference_client.infer_image(image_path)
    inference_client.save_results(result, output_path)