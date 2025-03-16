import streamlit as st
import requests
# import os
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

st.header("🔍 Search for a Book")
st.markdown('<div class="delete-box-2">', unsafe_allow_html=True)


search_query = st.text_input("Enter Book ID, Title, or Author Name")
if st.button("Search"):
    try:
        response = requests.get(f"{BASE_URL}/search_books/", params={"query": search_query})
        if response.status_code == 200:
            results = response.json()
            if results:
                st.table(results)
            else:
                st.write("No matching books found.")
        else:
            st.error(f"Search failed: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()


st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="delete-box">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()