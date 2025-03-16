import streamlit as st
import requests
# import os
import time
# from dotenv import load_dotenv

# load_dotenv()

# BASE_URL = os.getenv("BASE_URL" ,"")
BASE_URL="https://baitulhikmabooklab20-production.up.railway.app/"



st.divider()


st.header("📌 Update Read Status")
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


update_query = st.text_input("Enter Book ID, Title, or Author Name", key="update_read_status")
new_status = st.checkbox("Mark as Read")
if st.button("Update Status"):
    try:
        # FIXED: Correct URL format for update endpoint
        response = requests.put(f"{BASE_URL}/update_read_status/", 
            params={"query": update_query, "read_status": new_status})
        if response.status_code == 200:
            st.success("Status updated!",icon="✅")
            st.toast("Status updated!")
            st.toast("Book read status updated ")
            st.balloons()
            time.sleep(2)
            st.session_state.update_state = ""
            st.rerun()
        else:
            st.error(f"Update failed: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="delete-box">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

