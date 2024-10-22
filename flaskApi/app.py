import pandas as pd
from flask import Flask, request, jsonify
import jwt
import requests
from flask_cors import CORS
from pymongo import MongoClient
from models.content_based_filtering import content_based_filtering_history
from models.browsing_history import content_based_filtering_browsing_history
from models.reverse_image_search import get_image_recommendation
import asyncio
import aiohttp
import base64
import os
from tryon import try_on
from gen_ai import send_request_to_gemini, send_request_to_openai_image_gen, summarize_conversation, get_recommendation_keywords
from scraper import get_product_details
from trend_scraper import scrape_trends

app = Flask(__name__)
CORS(app, supports_credentials=True)
token_secret="2Z3SeD5FYpJ7ARSrjRrgyleAxmUDWLPUkCftQp"
mongo_client = MongoClient('mongodb+srv://StealthMode:ehfjZVeARoqO3Elb@stealthmode.mggqpgd.mongodb.net/?retryWrites=true&w=majority&appName=StealthMode') 
db = mongo_client['test'] 
users_collection = db['users'] 

base_url = 'http://localhost:8000/api/v4/'

@app.route('/content_based_filtering_cart_history', methods=['GET'])
def content_based_filtering_cart_history_post():
    # try:
        cookie = request.cookies['auth-token']
       
        decoded_payload = jwt.decode(cookie, token_secret, algorithms=['HS256'], verify=False)
        userId = decoded_payload['userId']
        age = decoded_payload['age']
        gender = decoded_payload['gender']
        city = decoded_payload['city']

        response = requests.get(f"{base_url}cartHistory/getCartHistory/{userId}")
        data = response.json()

        # Remove 'occasion' key from each object in the list
        filtered_data = []
        for item in data['data']:
            if 'occasion' in item:
                del item['occasion']
            if 'productName' in item:
                del item['productName']
            filtered_data.append(item)

        urls = content_based_filtering_history(filtered_data, str(userId), age, gender, city, 'cartDate')

        productsPayload = {"productsData" : urls[0]}
        res = requests.put(f"{base_url}cartHistory/addToRecommendedCart/{userId}", json=productsPayload)
        print(res.json())
        
        imagesPayload = {"imagesUrl" : urls[1]}
        res = requests.put(f"{base_url}cartHistory/addToGeneratedCart/{userId}", json=imagesPayload)
        print(res.json())

        print(urls)
        return jsonify(decoded_payload)
    # except Exception as e:
    #     return jsonify({'message': 'Unauthorised'}), 400

@app.route('/content_based_filtering_browsing_history', methods=['GET'])
def content_based_filtering_browsing_history_post():
    # try:
        cookie = request.cookies['auth-token']
        # Check if cookie is present if not return error
        if not cookie:
            return jsonify({'message': 'Unauthorised'}), 400
        
        decoded_payload = jwt.decode(cookie, token_secret, algorithms=['HS256'], verify=False)
        userId = decoded_payload['userId']
        age = decoded_payload['age']
        gender = decoded_payload['gender']
        city = decoded_payload['city']

        response = requests.get(f"{base_url}browsingHistory/getBrowsingHistory/{userId}")
        data = response.json()

        # Remove 'occasion' key from each object in the list
        filtered_data = []
        for item in data['data']:
            if 'occasion' in item:
                del item['occasion']
            if 'productName' in item:
                del item['productName']
            filtered_data.append(item)

        urls = content_based_filtering_browsing_history(filtered_data, str(userId), age, gender, city)

        # insert url to mongodb database
        productsPayload = {"productsData" : urls[0]}
        res = requests.put(f"{base_url}browsingHistory/addToRecommendedBrowsing/{userId}", json=productsPayload)
        print(res.json())
        
        imagesPayload = {"imagesUrl" : urls[1]}
        res = requests.put(f"{base_url}browsingHistory/addToGeneratedBrowsing/{userId}", json=imagesPayload)
        print(res.json())

        # print the urls
        print(urls)
        return jsonify(decoded_payload), 200
    # except Exception as e:
    #     return jsonify({'message': 'Unauthorised'}), 400

@app.route('/content_based_filtering_purchasing_history', methods=['GET'])
def content_based_filtering_purchasing_history_post():
    # try:
        cookie = request.cookies['auth-token']
        decoded_payload = jwt.decode(cookie, token_secret, algorithms=['HS256'], verify=False)
        userId = decoded_payload['userId']
        age = decoded_payload['age']
        gender = decoded_payload['gender']
        city = decoded_payload['city']

        response = requests.get(f"{base_url}purchasingHistory/getPurchasing/{userId}")
        data = response.json()

        # Remove 'occasion' key from each object in the list
        filtered_data = []
        for item in data['data']:
            if 'occasion' in item:
                del item['occasion']
            if 'productName' in item:
                del item['productName']
            filtered_data.append(item)

        urls = content_based_filtering_history(filtered_data, str(userId), age, gender, city, 'purchaseDate')

        productsPayload = {"productsData" : urls[0]}
        res = requests.put(f"{base_url}purchasingHistory/addToRecommendedPurchasing/{userId}", json=productsPayload)
        print(res.json())
        
        imagesPayload = {"imagesUrl" : urls[1]}
        res = requests.put(f"{base_url}purchasingHistory/addToGeneratedPurchasing/{userId}", json=imagesPayload)
        print(res.json())

        print(urls)
        return jsonify(decoded_payload), 200
    # except Exception as e:
    #     return jsonify({'message': 'Unauthorised'}), 400

@app.route('/content_based_filtering_frequentData_history', methods=['GET'])
def content_based_filtering_frequentData_history_post():
    # try:
        cookie = request.cookies['auth-token']
        print("cookie", cookie)
        decoded_payload = jwt.decode(cookie, token_secret, algorithms=['HS256'], verify=False)
        userId = decoded_payload['userId']
        age = decoded_payload['age']
        gender = decoded_payload['gender']
        city = decoded_payload['city']

        print(userId)

        response = requests.get(f"{base_url}frequentData/getFrequentData/{userId}")
        data = response.json()
        print("data", data)

        # Remove 'occasion' key from each object in the list
        filtered_data = []
        for item in data['data']:
            if 'occasion' in item:
                del item['occasion']
            if 'productName' in item:
                del item['productName']
            filtered_data.append(item)

        urls = content_based_filtering_history(filtered_data, str(userId), age, gender, city, 'viewDate')
        productsPayload = {"productsData" : urls[0]}
        res = requests.put(f"{base_url}frequentData/addToRecommendedFrequentData/{userId}", json=productsPayload)
        print(res.json())
        
        imagesPayload = {"imagesUrl" : urls[1]}
        res = requests.put(f"{base_url}frequentData/addToGeneratedFrequentData/{userId}", json=imagesPayload)
        print(res.json())

        print(urls)
        return jsonify(decoded_payload), 200
    # except Exception as e:
    #     return jsonify({'message': 'Unauthorised'}), 400

@app.route('/get_image_id', methods=['POST'])
def get_image_id():
    # try:
        # get image url from body
        print("Initialising image recommendation")
        image_url = request.json['imageUrl']

        image_id = get_image_recommendation(image_url)

        return jsonify({"image_id": image_id}), 200
    # except Exception as e:
    #     return jsonify({'message': 'Unauthorised'}), 400

@app.route('/virtual_try_on', methods=['POST'])
async def virtual_try_on():
    try:
        print("Initialising virtual try on")

        productId = request.json.get('productId')
        category = request.json.get('category')
        print(productId)
        print(category)

        if not productId:
            return jsonify({'message': 'Product path is required'}), 400

        cookie = request.cookies.get('auth-token')
        if not cookie:
            return jsonify({'message': 'Missing auth token'}), 600

        try:
            decoded_payload = jwt.decode(cookie, token_secret, algorithms=['HS256'], verify=False)
            user_id = decoded_payload.get('userId')
        except jwt.DecodeError:
            return jsonify({'message': 'Invalid token'}), 401

        if not user_id:
            return jsonify({'message': 'User ID not found in token'}), 401

        user_data = users_collection.find_one({'userId': user_id})
        if not user_data or 'imageUrl' not in user_data:
            return jsonify({'message': 'Image URL not found for this user'}), 404

        img_url = user_data['imageUrl']

        base_image_folder = '../website/server/product_images/extracted_images/'
        product_image_filename = f"{productId}_extracted.png"
        product_image_path = os.path.join(base_image_folder, product_image_filename)

        print(f"Product image path: {product_image_path}")
        print(f"User image URL: {img_url}")

        if category == 'Topwear':
            category = 'Upper body'
        elif category == 'Bottomwear':
            category = 'Lower body'
        else:
            category = 'Lower body'

        result = await try_on(cloth_image_path=product_image_path, person_image_path=None, cloth_image_url= None, person_image_url=img_url, clothing_category=category)

        print(result+" is the result")
        return jsonify({'message': 'Virtual try on successful', 'imagePath': result}), 200


    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'message': 'Unauthorised'}), 400

user_conversations = {}

@app.route('/conversation', methods=['POST'])
def handle_conversation():
    data = request.json
    user_id = data.get('userId')
    message = data.get('message')

    if message.strip().lower().startswith("/generate"):
        prompt = message.strip().lower().replace("/generate", "").strip()

        summary = None
        conversation_history = [entry["message"] for entry in user_conversations.get(user_id, [])]
        if len(conversation_history) > 1:
            summary = summarize_conversation(" ".join(conversation_history))
            print("Prompt after summarization: ", summary)
            
            summary = summarize_conversation(conversation_history)
        
        if summary:
            prompt = summary
        
        text = (
    f"Generate a single photorealistic outfit based on the following description: {prompt}. "
    "The image should feature only one clothing item, focusing on its design, texture, and color. "
    "The background must be strictly white, with no person, accessories, or additional outfits present. "
    "Ensure that only one outfit is shown clearly, without any extra elements or context."
)
        print("Prompt for image gen: ", text)
        image_url = send_request_to_openai_image_gen(text)

        return jsonify({"response": image_url})
    
    elif message.strip().lower().startswith("/recommend"):
        prompt = message.strip().lower().replace("/recommend", "").strip()

        summary = None
        conversation_history = [entry["message"] for entry in user_conversations.get(user_id, [])]
        if len(conversation_history) > 1:
            summary = summarize_conversation(" ".join(conversation_history))
            print("Prompt after summarization: ", summary)
            
            summary = get_recommendation_keywords(conversation_history)
            
        if summary:
            prompt = summary
            
        product_details = get_product_details(prompt)
        
        return jsonify({"response": product_details})

    if user_id not in user_conversations:
        user_conversations[user_id] = []

    user_conversations[user_id].append({"message": message, "from": "user"})

    conversation_history = [entry["message"] for entry in user_conversations[user_id]]
    
    summary = None
    if len(conversation_history) > 1:
        summary = summarize_conversation(" ".join(conversation_history))
        print("Prompt after summarization: ", summary)
        
    if summary:
        prompt = summary
    else:
        prompt = message
    print("Prompt: ", prompt)

    response = send_request_to_gemini(prompt, app.config['TRENDS_JSON'])

    user_conversations[user_id].append({"message": response, "from": "ai"})

    return jsonify({"response": response})

# API to clear the conversation history/memory
@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    user_id = request.json.get('userId')
    user_conversations[user_id] = []
    return jsonify({"message": "Chat history cleared"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Healthy"})

@app.before_request
def startup():
    print("Starting up...")
    url = "https://iifd.in/the-future-of-style-top-5-emerging-fashion-trends-for-2024/"
    trends_json = scrape_trends(url)
    summary = summarize_conversation(trends_json)
    app.config['TRENDS_JSON'] = summary

if __name__ == '__main__':
    app.run(debug=True)
