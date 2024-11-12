import streamlit as st
from decoding_QR import decode_qrcode_page
from qrcode_generator1 import generate_qrcode_page

st.set_page_config(page_title="QR Code App",
                   page_icon='🐬')

#create a sider  bar with some pages
options = ['Create QR Code', 'Decodes QR Code', 'About Me']
page_selection = st.sidebar.selectbox("Menu",
                                      options)

if page_selection == "Create QR Code":
   generate_qrcode_page()
elif page_selection == "Decodes QR Code":
    decode_qrcode_page()
elif page_selection == "About Me":
    st.write("Hi, my name is Alex!")