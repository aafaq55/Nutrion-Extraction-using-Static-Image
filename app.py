### Health Management APP

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini Pro Vision API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Health App")

# Header
st.title("Nutrition Calculation using Static Image")
st.write("Welcome to Gemini Health App, where you can analyze the nutritional content of your food images.")

# File uploader for image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Button to analyze image
    if st.button("Analyze Image"):
        input_prompt = """
        You are an expert nutritionist tasked with analyzing the food items from the image and calculating the total calories.
        Provide details of each food item along with its calorie intake in the following format:

        1. Item 1 - no of calories
        2. Item 2 - no of calories
        ...

        Additionally, mention whether the food is healthy or not, and provide the percentage split of carbohydrates, fats, fibers, sugar, and other important dietary components.
        """

        try:
            # Analyze image and get response
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)

            # Display response
            st.subheader("Analysis Results:")
            st.write(response)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
