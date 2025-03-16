import streamlit as st
import requests
# import os
import time
# from dotenv import load_dotenv

# load_dotenv()

# BASE_URL = os.getenv("BASE_URL" ,"")
BASE_URL="https://baitulhikmabooklab20-production.up.railway.app/"


st.divider()
st.markdown(
    """
    <style>
    .delete-box {
        background-color: #1E1E1E;        
        height: 40px;
        padding: 20px;
        border-radius: 10px 0px 10px 0px  ;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-bottom:30px
    }
    .delete-box-2 {
        background-color: #FFCA28;        
        min-height: 120px;
        padding: 20px;
        border-radius: 10px 0px 10px 0px  ;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-bottom:30px
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("➕ Add a Book")
st.markdown('<div class="delete-box-2">', unsafe_allow_html=True)

title = st.text_input("Book Title")
author = st.text_input("Author Name")
# genre = st.text_input("Genre")
genre = st.selectbox("Genre" ,[ "Science Fiction", "Mystery/Thriller", "Historical", "Horror", "Action/Adventure"], key="add_genre")
publication_year = st.number_input("Publication Year", min_value=1000, max_value=3000, step=1)
if st.button("Add Book"):
    data = {"title": title, "author": author, "genre": genre, "publication_year": publication_year}
    try:
        response = requests.post(f"{BASE_URL}/add_book/", params=data)
        if response.status_code == 200:
            st.session_state.clear()
            st.success("Book added successfully!",icon="✅")
            st.balloons()
            time.sleep(2)
            st.session_state.add_title = ""
            st.session_state.add_author = ""
            st.session_state.add_year = 1500  # Reset to min_value or a default
            st.rerun()
        else:
            st.error(f"Failed to add book: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="delete-box">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()
