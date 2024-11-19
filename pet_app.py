import streamlit as st
import requests

st.set_page_config(page_title="My Pet App",
                   page_icon="🐹")

st.header("Welcome to my Pet App!!!",
          divider='rainbow')

def get_cat_image():
    url = "https://cataas.com//cat"
    contents = requests.get(url)

    return contents.content

def get_dog_image():
    url = "https://random.dog/woof.json"
    contents = requests.get(url).json()
    dog_image_url = contents['url']

    return dog_image_url

c1, c2 = st.columns(2)

with c1:
    cat_button = st.button("Click here to see a 🐈")
    if cat_button:
        cat_image = get_cat_image()
        st.image(cat_image)

with c2:
    dog_button = st.button("Click here to see a 🐶")
    if dog_button:
        dog_image = get_dog_image()
        st.image(dog_image)