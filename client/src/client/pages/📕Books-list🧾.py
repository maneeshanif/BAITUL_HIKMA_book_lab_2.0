import streamlit as st
import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# BASE_URL = os.getenv("BASE_URL" ,"")
BASE_URL="https://baitulhikmabooklab20-production.up.railway.app/"

# Function to fetch books
def get_books():
    try:
        response = requests.get(f"{BASE_URL}/get_books/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get books: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []
    



st.header("📖 Book List")
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

st.markdown('<div class="delete-box-2">', unsafe_allow_html=True)


# Fetch and display books
# st.subheader("📖 Book List")
books = get_books()
if books:
    st.table(books)
else:
    st.write("No books found.")

st.divider()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="delete-box">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()
