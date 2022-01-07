import streamlit as st
import pandas as pd
from page_generate_random_img import show_img_random_generation_page
from page_generate_specific_img import show_img_specific_generation_page
from page_user import show_user_page


def show_home_page():
    title = "Home page"
    st.markdown(f"<h1 style='text-align: center;'>{title}", unsafe_allow_html=True)
    # st.markdown(":house:")

    colA, colB, colC = st.columns([1,1,1])
    page_random = colA.button("Generate random images 🎲")
    page_specific = colB.button("Generate specific images 🎯")
    page_user = colC.button("Who would you look like.. ? 🔮")

    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #f44336;         /* Red */
        color:#ffffff;
        transition-duration: 0.4s;
    }
    div.stButton > button:hover {
        background-color: #4CAF50;        /* Green */
        color: white;
        }
    </style>""", unsafe_allow_html=True)

    page = "Home 🏠"
    if page_random:
        page = "Generate random images 🎲"
    elif page_specific:
        page = "Generate specific images 🎯"
    elif page_user:
        page = "Who would you look like.. ? 🔮"

    return page
