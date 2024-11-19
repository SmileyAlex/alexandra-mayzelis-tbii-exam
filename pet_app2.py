import streamlit as st
import requests
import random

# Replace with your Unsplash API key
api_key = st.secrets['unsplash_api_key']


def get_images(query, api_key, results=10):
    """Code from chatgpt to fetch image URLs based on a query."""
    search_url = "https://api.unsplash.com/search/photos"
    response = requests.get(search_url,
                            params={"query": query.lower(), "client_id": api_key, "per_page": results})
    return [img["urls"]["regular"] for img in response.json().get("results", [])]


# Get animal image
# create a text box in streamlit
animal = st.text_input("What animal would you like to see a picture of?")
if animal:
    try:
        animal_images = get_images(animal, api_key)
        animal_image = random.choice(animal_images)
        st.image(animal_image, width=300, caption=f"My {animal.capitalize()} image")
    except:
        st.warning("Animal does not exist")