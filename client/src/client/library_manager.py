
import streamlit as st
import os

st.set_page_config(page_title="BAITUL_HIKMA_2.0",page_icon="📖")
st.title("📚 BAITUL HIKMA")
st.markdown(
    """
    <h4 style='text-align: center; color: #FFCA28; margin-top: -10px;'>
        A Full-Stack Library Solution<br>Powered by Streamlit, FastAPI & PostgreSQL
    </h4>
    """,
    unsafe_allow_html=True
)


# Custom CSS for styling
st.markdown(
    """
    <style>
    .highlight {
        color: #FFCA28;  /* Yellow accent */
        font-weight: bold;
    }
    .author {
        text-align: center;
        font-size: 18px;
        color: #FF5733;  /* Orange for your name */
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)



image_path = os.path.abspath("./images/library2.jpg")


# Check if the file exists
if os.path.exists(image_path):
    st.image(image_path, width=630)
else:
    st.warning(f"Image not found: {image_path}. Using a placeholder instead.")
    st.image("https://media.istockphoto.com/id/1015149600/photo/book-hall-in-library.jpg?s=2048x2048&w=is&k=20&c=un9XrdxJMA4Lpa5s91IfWlUSiujtbEwVx8ewxlxBZQo=", width=630)  # Placeholder image

# st.image(image_path, width=630)


# st.image("./images/library2.jpg", width=630 )

# Features and Tech Stack Section
st.markdown(
    """
    <h3>Welcome to BAITUL_HIKMA Library Manager!</h3>
    <p>This is <span class="highlight">Version 2</span> of the Book Library Manager, an enhanced tool to organize your reading collection efficiently. Here are its key features:</p>
    <ul>
        <li><b>Add Books</b>: Enter new titles, authors, genres, and publication years.</li>
        <li><b>Remove Books</b>: Delete books from your collection with ease.</li>
        <li><b>Track Progress</b>: Monitor your reading progress with a clear pie chart.</li>
    </ul>
    <p><span class="highlight">Tech Stack:</span> Built with <b>Streamlit</b> for the frontend, <b>FastAPI</b> for the backend API, and <b>PostgreSQL</b> for data storage. It’s robust, scalable, and efficient.</p>
    <p><span class="highlight">What’s New:</span> Version 2 brings a full-stack architecture, improved performance, and a more responsive interface. More features are on the way!</p>
    """,
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Author Credit
st.markdown('<p class="author">Created by Maneeshanif</p>', unsafe_allow_html=True)
st.divider()