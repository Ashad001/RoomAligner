import json

def preprocess_data(data):
    inference_id = data.get("inference_id", "N/A")
    time_taken = data.get("time", "N/A")
    image_width = data["image"].get("width", "N/A")
    image_height = data["image"].get("height", "N/A")
    
    description = (f"Image Dimensions: {image_width}x{image_height}\n"
                   f"Detected Objects:\n")

    for idx, prediction in enumerate(data["predictions"], start=1):
        x = prediction.get("x", "N/A")
        y = prediction.get("y", "N/A")
        width = prediction.get("width", "N/A")
        height = prediction.get("height", "N/A")
        confidence = prediction.get("confidence", "N/A")
        detected_class = prediction.get("class", "N/A")
        class_id = prediction.get("class_id", "N/A")
        detection_id = prediction.get("detection_id", "N/A")
        
        if confidence > 0.5:
            description += (f"\nDetection {idx}:\n"
                            f"- Class: {detected_class} (ID: {class_id})\n"
                            f"- Bounding Box: Center({x}, {y}), Width: {width}, Height: {height}\n"
                            f"- Confidence: {confidence:.2f}\n")

    return description

