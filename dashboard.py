import streamlit as st
import pandas as pd
import numpy as np

st.title("Dashboard Berumen")
st.header("Section Header")
st.subheader("Subsection")
st.write("Marckdown, Numbers, Dataframes , Floats, strs")
st.markdown("**Bold**")

name = st.text("Model Name")
optiones = st.selectbox("Choose a model", ["CNN", "RNN", "YOLO", "DIFFUSION"])
threshhold  = st.slider ("cinfidence threshhold",0.0,1.0,1.5)
red_button  = st.button("Run Influence")


df = pd.DataFrame(np.random.randn(20,3), columns=["a", "b", "c"])
st.dataframe(df)
st.line_chart(df)
