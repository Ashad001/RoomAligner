#### **Overview**

Welcome to the documentation for interacting with the **RoomAligner API**, which is hosted at [https://ashad001-roomaligner.hf.space](https://ashad001-roomaligner.hf.space). This API helps generate room structure suggestions based on uploaded images of room plans.

---

### **Embedding the API**

For embedding the API in an application or webpage, you can use an iframe as follows:

```html
<iframe
  src="https://ashad001-roomaligner.hf.space"
  frameborder="0"
  width="850"
  height="450"
></iframe>
```

---

### **Available Endpoints**

#### 1. **Upload Room Image and Get Suggestions**

- **Endpoint**: `/upload-room-image/`
- **Method**: `POST`
- **Description**: This endpoint accepts an image of a room plan, processes it to classify objects, generates a natural language description, and provides suggestions for room structure improvement.

#### **Request Format**

- **URL**: `/upload-room-image/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: The room plan image file (JPEG format).

#### **Example Request (cURL)**

```bash
curl -X POST "https://ashad001-roomaligner.hf.space/upload-room-image/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.jpg"
```

#### **Response**

If the request is successful, the API returns a JSON response with:
- Natural language description of the room plan.
- The current room structure.
- Suggested room structure for better flow and space utilization.

#### **Example Response**

```json
{
  "natural_language_description": "The room contains a sofa, coffee table, and TV. The layout is suitable for a small living room.",
  "room_structure": "Current room layout includes the following furniture: Sofa (center), TV (front), Coffee Table (middle).",
  "suggested_structure": "We suggest moving the coffee table closer to the seating area and positioning the TV on the right wall to improve flow."
}
```

#### **Error Responses**

- **500 Internal Server Error**: If something goes wrong while processing the image or generating suggestions, the API will return an error message in JSON format.

```json
{
  "detail": "An error occurred: <error details>"
}
```

---

### **Frontend Interaction Guide**

To interact with the API, follow these steps:

1. **File Upload**:
   - Use an `HTML <input>` element with `type="file"` to allow users to upload the image of the room.
   
   ```html
   <input type="file" id="roomImage" accept="image/jpeg">
   ```

2. **API Request**:
   - Use JavaScript's `FormData` to package the uploaded image.
   - Send a `POST` request to the `/upload-room-image/` endpoint using `fetch()` or any preferred HTTP client (e.g., Axios).

   **Example Using JavaScript's Fetch API**:

   ```javascript
   const uploadImage = async () => {
       const fileInput = document.getElementById('roomImage');
       const formData = new FormData();
       formData.append('file', fileInput.files[0]);

       try {
           const response = await fetch('https://ashad001-roomaligner.hf.space/upload-room-image/', {
               method: 'POST',
               body: formData
           });

           const result = await response.json();
           console.log('Natural Language Description:', result.natural_language_description);
           console.log('Current Room Structure:', result.room_structure);
           console.log('Suggested Room Structure:', result.suggested_structure);
       } catch (error) {
           console.error('Error uploading image:', error);
       }
   };
   ```

3. **Handle the Response**:
   - Parse the JSON response and display the results on your webpage. You can show the natural language description, current room structure, and suggestions for improving the room layout.

---

### **CORS Policy**

CORS is enabled on the API, allowing requests from any origin (`*`). Therefore, frontend applications can make cross-origin requests directly without additional configuration.
