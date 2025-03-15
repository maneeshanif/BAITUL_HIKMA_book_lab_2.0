import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL" ,"")

# Delete a book

st.divider()
st.header("🗑️ Trash a Book", anchor="delete")
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


delete_query = st.text_input("Enter Book ID, Title, or Author Name to Remove")
if st.button("Delete Book"):
    try:
        # FIXED: Correct URL format for delete endpoint
        response = requests.delete(f"{BASE_URL}/delete_book/", 
                params={"query": delete_query})
        if response.status_code == 200:
            st.success("Book yeeted successfully!", icon="✅")
            st.toast("Book’s gone, bro!", icon="🗑️")
            st.balloons()
            time.sleep(1)
            st.session_state.delete_state = ""
            st.rerun()
        else:
            st.error(f"Deletion failed: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")


st.divider()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="delete-box">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()
