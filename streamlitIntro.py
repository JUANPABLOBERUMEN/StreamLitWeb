import streamlit as st

name = st.text_input("Your Name","Berumen")
age = st.slider("Your Age", 0,100,25)

st.write(f"Hola, {name}. Tienes {age} años.")