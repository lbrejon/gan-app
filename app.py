import streamlit as st
from streamlit.elements.form import current_form_id
from page_home import show_home_page
from page_generate_random_img import show_img_random_generation_page
from page_generate_specific_img import show_img_specific_generation_page
from page_user import show_user_page
from keras.preprocessing.image import load_img

import base64


if 'status' not in st.session_state:
    st.session_state['status'] = True
    st.session_state['nb_loaded_pages'] = 0
    st.session_state['page1'] = dict()
    st.session_state['page2'] = dict()
    st.session_state['page3'] = dict()

main_bg = "img/logoEMMK.png"
main_bg_ext = "png"

# img_logo = load_img(main_bg)
# st.sidebar.image(img_logo)

pages = ["Home 🏠", "Generate random images 🎲", "Generate specific images 🎯", "Who would you look like.. ? 🔮"]

# new_page_sidebar = st.sidebar.selectbox("Choose your page:", (pages[0], pages[1], pages[2], pages[3]))
sidebar_page = st.sidebar.selectbox("Choose your page:", (pages[1], pages[2], pages[3]))
if st.session_state['status']:
    st.session_state['current_page'] = sidebar_page
    st.session_state['nb_loaded_pages'] += 1
    # st.write(st.session_state)


if st.session_state['current_page'] == pages[1]:
    data = show_img_random_generation_page()
elif st.session_state['current_page'] == pages[2]:
    show_img_specific_generation_page()
elif st.session_state['current_page'] == pages[3]:
    show_user_page()
