import requests
import google.generativeai as genai
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def send_request_to_gemini(message):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "You are a professional fashion assistant. Help users find the perfect outfits based on their preferences, occasion, and style. Focus on clothing types, fabrics, colors, and outfit combinations. Keep responses concise, no more than 100 words. Don't ask for personal information or any other data. Provide general advice and recommendations."
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
    prompt = f"Summarize the following conversation: {conversation}"
    prompt += "\nSummarize the conversation in 1-2 sentences. The goal is to capture essential fashion details (clothing type, style, color, occasion) and remove extraneous information."
    print("Prompt for summarization: ", prompt)
    response = model.generate_content(prompt)
    return response.text

def get_recommendation_keywords(message):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Extract the product recommendation from the following conversation: {message}."
    prompt += "\nIdentify and output only 1 clothing/fashion-related keyword or phrases that represent the user's preferences or needs."
    
    response = model.generate_content(prompt)
    return response.text