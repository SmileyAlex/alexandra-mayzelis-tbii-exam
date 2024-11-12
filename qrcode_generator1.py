import streamlit as st
import segno
import time

def generate_qrcode_page():
    # place an image
    # you can either download an image, or include the image file path
    st.image("waves_image.jpg")

    # place a title
    st.title("THE QR CODE GENERATOR")

    # place a text input box
    url = st.text_input("Enter the data you would like to encode")

    # Thank you to Refiye for suggesting this
    # option 1 - ask the user for a colour
    # dark_colour = st.text_input("What colour would like the dark squares to be?")

    # Thanks Jannik and Finn for the colour picker
    # option 2, use a colour picker but it defaults to black
    dark_colour = st.color_picker("Pick a colour for the dark squares", "#8569a8")

    # thanks Aneeka for suggesting we could create a button
    button = st.button("Click here to generate")

    # definition that creates the qr code
    def generate_qrcode(url, dark_colour):
        qrcode = segno.make_qr(url)
        qrcode.to_pil(scale=10,
                      dark=dark_colour).save("qrcode_streamlit.png")

    # when the user clicks on the button and have entered a url
    if button and url:
        # create a spinner if you want to
        with st.spinner("Generate QR Code"):
            time.sleep(1.5)
        # generate a qr code
        generate_qrcode(url, dark_colour)
        # place the qr code
        st.image("qrcode_streamlit.png",
                 caption="My Generate QR Code")

    # warning for when user clicks on button without a url
    if button and url == "":
        st.warning("Please enter the data you would like to encode")

    # you can play around with markdowns
    # check out the code in github
    st.markdown(
        "<br><hr><center>Made with ❤️ by <a href='mailto:sarah.haq@leuphana.de?subject=QRCode Generator WebApp!&body=Please specify the issue you are facing with the app.'><strong>Sarah Haq</strong></a><br><br>Sarah is a Lecturer at Leuphana Uni and avid Pythonista.</center><hr>",
        unsafe_allow_html=True)
