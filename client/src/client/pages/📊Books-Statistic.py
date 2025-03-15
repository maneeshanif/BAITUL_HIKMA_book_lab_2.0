import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px


load_dotenv()

BASE_URL = os.getenv("BASE_URL" ,"")

st.header("📈 My Reading Stats", anchor="stats")



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
    
books = get_books()


if books:
    # Calculate stats
    read_books = sum(1 for book in books if book.get("read_status"))
    total_books = len(books)
    progress = read_books / total_books if total_books > 0 else 0

    #  progress bar
    st.markdown(
        """
        <style>
        .stProgress > div > div > div > div {
            background-color: #FF6F61; /* Coral red for progress */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.progress(progress)
    
    # Header div 
    st.markdown(
        f"""
        <div style='background-color: #1E1E1E; padding: 15px; border-radius: 10px; text-align: center; color: #FFFFFF;'>
            <h3 style='margin: 0; color: #FFCA28;'>Library Snapshot</h3>
            <p style='font-size: 18px; margin: 5px 0;'>Total Books: <b>{total_books}</b> | Read: <b>{read_books}</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    #  sub heading
    st.markdown("<h4 style='color: #FFCA28;'>Read vs Unread Breakdown</h4>", unsafe_allow_html=True)
    pie_data = [
        {"Status": "Read", "Count": read_books},
        {"Status": "Unread", "Count": total_books - read_books}
    ]
    pie_df = pd.DataFrame(pie_data)

    fig = px.pie(
        pie_df, 
        values="Count", 
        names="Status", 
        color_discrete_sequence=["#00C4B4", "#FF5733"],  # Teal and orange
        hole=0.5,  # Bigger donut hole
        opacity=0.9
    )
    fig.update_traces(
        textinfo="percent+label", 
        marker=dict(line=dict(color="#FFFFFF", width=2))  # White borders
    )
    # just try to figure out below function later
    # fig.update_layout(
    #     plot_bgcolor="rgba(0,0,0,0)", 
    #     paper_bgcolor="rgba(0,0,0,0)", 
    #     font=dict(color="#FFFFFF", size=14),
    #     margin=dict(t=20, b=20, l=20, r=20),
    #     legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    # )
    # main function who is responsible for creating and updating our pie
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No books in the library yet. Add some to see your stats!")


st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="delete-box">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()