from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import io
from PIL import Image
import uuid
import firebase_admin
from firebase_admin import credentials, storage
from .firebase_init import initialize_firebase, firebase_initialized

class ActionGenerateOutfit(Action):
    def name(self) -> Text:
        return "action_call_api"
    
    def __init__(self):
        super(ActionGenerateOutfit, self).__init__()
        initialize_firebase('D:\\Projects\\Flipkart GRiD 5.0\\new\\fashionkart\\chatbot\\actions\\firebase-admin-sdk.json', 'fashionkart-26db7.appspot.com')

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        age = tracker.get_slot("age")
        gender = tracker.get_slot("gender")
        location = tracker.get_slot("location")
        occasion = tracker.get_slot("occasion")
        category = tracker.get_slot("category")

        input_prompt = f"My location is {location}, my age is {age} and gender is {gender}. Generate {category} with  color for {occasion} occasion."
        image_url = self.generate_image(input_prompt)

        dispatcher.utter_message(
            text=f"Here's an outfit suggestion for you:\n"
        )

        image_attachment = {"image": image_url}

        dispatcher.utter_message(attachment=image_attachment)

        return []

    def query(self, payload):
        try:
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
            headers = {"Authorization": "Bearer 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"}
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.content
        except requests.exceptions.RequestException as e:
            print("Error making API request:", e)
            return None

    def generate_image(self, prompt):
        image_bytes = self.query({
            "inputs": f"{prompt}",
        })
        image = Image.open(io.BytesIO(image_bytes))

        # Save the image temporarily before uploading
        temp_image_path = "output.jpg"
        image.save(temp_image_path)

        # Upload the image and get the URL
        firebase_uploader = FirebaseUploader()
        image_url = firebase_uploader.upload_to_firebase(temp_image_path, 'generatedImages')

        return image_url

class FirebaseUploader:
    def upload_to_firebase(self, image_path, folder_name):
        bucket = storage.bucket()
        destination_blob_name = f"{folder_name}/{str(uuid.uuid4())}.jpg"
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(image_path)

        blob_url = blob.public_url
        return blob_url
