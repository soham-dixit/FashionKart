import requests
import google.generativeai as genai
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def send_request_to_gemini(message, trends):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"You are a professional fashion assistant. Help users find the perfect outfits based on their preferences, occasion, and style. Focus on clothing types, fabrics, colors, and outfit combinations. Keep responses concise, no more than 100 words. Don't ask any questions. Provide general advice and recommendations. Given below are some latest fashion trends for 2024. Use these trends to guide your responses. It is in json format. {trends}"
    prompt += f"\nThe user says: {message}"
    print("Prompt for Gemini: ", prompt)
    response = model.generate_content(prompt)
    return response.text

def send_request_to_openai_image_gen(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    return response.data[0].url

def summarize_conversation(conversation):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = (
        "Summarize the following conversation with a focus on fashion-related details. "
        "Extract precise information about the type of clothing, style, color, fabric, occasion, and any specific design elements mentioned. "
        "Exclude any irrelevant or non-fashion details. Ensure the summary is concise and structured in a way that can be used as input for generating an accurate fashion image."
    )
    prompt += f"\nConversation: {conversation}"
    prompt += "\nSummarize the fashion elements in 1-2 sentences, avoiding any unnecessary context or extraneous information. Just provide the key fashion details. Dont ask any questions and never begin the summary like 'The conversation is about...'"
    
    response = model.generate_content(prompt)
    return response.text

def get_recommendation_keywords(message):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Extract the product recommendation from the following conversation: {message}."
    prompt += "\nIdentify and output only 1 clothing/fashion-related keyword or phrases that represent the user's preferences or needs."
    
    response = model.generate_content(prompt)
    return response.text