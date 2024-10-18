# RoomAligner

RoomAligner is an AI-powered interior design assistant that helps users optimize room layouts for better flow and space utilization. By analyzing floor plan images, RoomAligner provides intelligent suggestions on how to rearrange furniture, identify potential space optimizations, and improve room functionality. It leverages advanced AI models to understand room structures and offer personalized design insights.

## Features
- **Object Detection**: Automatically detects objects (furniture, fixtures, etc.) from room floor plan images.
- **Natural Language Descriptions**: Transforms room data into a detailed natural language description, highlighting key features and layout.
- **Space Optimization Suggestions**: Provides intelligent suggestions to optimize room layouts by improving the arrangement of furniture and utilizing unused space.
- **Interactive UI**: Upload your floor plan image, get instant insights, and view optimized room layouts directly through the app interface.

## How It Works
1. **Upload an Image**: Users can upload a floor plan or room image in `.jpg` format.
2. **AI-Powered Object Detection**: RoomAligner detects and classifies objects in the image using a powerful inference model.
3. **Natural Language Description**: The tool generates a descriptive breakdown of the room’s current structure, identifying key furniture pieces and functional zones.
4. **Space Optimization**: Based on the room structure, RoomAligner suggests ways to improve space utilization, rearranging furniture for better flow and proposing enhancements.

## Installation
### Clone the Repository
```bash
git clone https://github.com/your-username/roomaligner.git
cd roomaligner
```

### Install Dependencies
Use the provided `requirements.txt` file to install the necessary Python packages.
```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file and add your API keys for Roboflow and OpenAI.
```plaintext
ROBOFLOW_API_KEY=your_roboflow_api_key
OPENAI_API_KEY=your_openai_api_key
```

### Run the App
```bash
streamlit run main.py
```

## Usage
1. Launch the app using Streamlit.
2. Upload an image of your room or floor plan.
3. View the detected objects and natural language description.
4. Get suggestions for improving your room layout with enhanced space optimization.

## Project Structure
- `raster/`: Contains the `InferenceClient` for detecting objects in the image.
- `plan/`: Includes the image analyzer and agent modules for generating descriptions and suggestions.
- `utils/`: Utility functions, including the data preprocessing pipeline.
- `main.py`: The main entry point for the Streamlit app.

## Contact
For questions, feedback, or contributions, feel free to reach out to:
- **Ashad Abdullah** – [GitHub](https://github.com/Ashad001) | [LinkedIn](https://linkedin.com/in/ashadqureshi1/)
