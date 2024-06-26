import pandas as pd
from flask import Flask, request, jsonify
import jwt
import requests
from flask_cors import CORS

from models.content_based_filtering import content_based_filtering_history
from models.browsing_history import content_based_filtering_browsing_history
from models.reverse_image_search import get_image_recommendation

app = Flask(__name__)
CORS(app, supports_credentials=True)
token_secret="2Z3SeD5FYpJ7ARSrjRrgyleAxmUDWLPUkCftQp"

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

if __name__ == '__main__':
    app.run(debug=True)
