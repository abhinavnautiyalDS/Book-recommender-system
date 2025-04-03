pip install streamlit==1.30.0 pandas==2.1.4 numpy==1.26.4 pickle-mixin==1.0.2 gdown


import streamlit as st
import pickle
import pandas as pd
import numpy as np
import base64
import gdown

# Google Drive file ID (Replace this with your actual file ID)
file_id = "191k7cqEm0JZmhdBujowlT9CroGTrWZ1c"


# Construct the direct download URL
url = f"https://drive.google.com/uc?id={file_id}"

# Download the file
output_path = "recommend.pkl"
gdown.download(url, output_path, quiet=False)


# Load the recommendation function and data
with open(output_path, "rb") as file:
    data_dict = pickle.load(file)

data = data_dict["data"]
similarity = data_dict["similarity"]
merge_df1 = data_dict["merge_df1"]

def search_books(query, merge_df1):
    """Find books matching the query (partial search)."""
    query = query.strip().lower()
    merge_df1["Book-Title"] = merge_df1["Book-Title"].str.strip().str.lower()
    results = merge_df1[merge_df1["Book-Title"].str.contains(query, na=False)]["Book-Title"].unique()
    return results[:5]  # Return top 5 matches

def recommend(book_name, data, similarity, merge_df1):
    # Normalize book name for matching
    book_name = book_name.strip().lower()
    
    # Normalize dataset index
    data.index = data.index.str.strip().str.lower()
    
    # Check if book exists in dataset
    if book_name not in data.index:
        st.warning(f"❌ '{book_name}' not found in dataset.")
        return []
    
    # Fetch index of the book
    index = np.where(data.index == book_name)[0][0]
    
    # Ensure similarity matrix shape matches data
    if similarity.shape[0] != len(data):
        st.error("⚠️ Similarity matrix size doesn't match dataset! Please check preprocessing.")
        return []
    
    # Get top 5 similar books
    similar_indices = np.argsort(-similarity[index])[1:6]
    book_titles = data.iloc[similar_indices].index.tolist()
    
    # Normalize book titles for matching
    merge_df1["Book-Title"] = merge_df1["Book-Title"].str.strip().str.lower()
    book_titles = [title.lower() for title in book_titles]
    
    # Filter book details
    info = merge_df1[merge_df1["Book-Title"].isin(book_titles)][
        ["Book-Title", "Book-Author", "Year-Of-Publication", "ISBN", "Image-URL-L"]
    ].drop_duplicates(subset="Book-Title", keep="first")
    
    return info.to_dict(orient="records")

#title 
st.set_page_config(layout="wide")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Replace with your local image file path (ensure it's in the same directory or provide full path)
image_base64 = get_base64_image("image (79).png")  # Change "background.jpg" to your image filename

# CSS for setting background image
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{image_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
</style>
"""

# Apply the background
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        body {
            background-image: url('https://drive.google.com/uc?id=11Xnm8X9TKP7tlvn9F7uL1CL-M3WPmm0r');
            background-size: cover;
        }

        .book-container {
            display: flex;
            justify-content: space-between;
            gap: 25px;
            flex-wrap: wrap;
        }

        .book-card {
            text-align: center;
            width: 18%;
            background: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            border: 2px solid black; /* Black border around book cards */
        }

        .book-card img {
            width: 100%;
            height: auto;
            border-radius: 10px;
        }

        .book-details {
            background: rgba(0, 0, 0, 0.8); /* Black background for better readability */
            color: white;
            font-size: 25px; /* Increase font size */
            padding: 8px;
            border-radius: 5px;
            display: inline-block;
            margin-top: 5px;
        }

        h1 {
            font-size: 60px !important; /* Increase title size */
            font-weight: bold;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("📚 Book Recommendation System")



# Session state to track selected book
if "selected_book" not in st.session_state:
    st.session_state.selected_book = ""

# User input for book name (search bar functionality)
st.markdown(
    """
    <style>
        /* Make the text input box bigger */
        .stTextInput>div>div>input {
            font-size: 20px !important; /* Increase font size */
            padding: 12px !important; /* More padding */
        }
    </style>
    """,
    unsafe_allow_html=True
)

query = st.text_input("📖 Enter a book title or keyword:", value=st.session_state.selected_book)


if query:
    matched_books = search_books(query, merge_df1)
    selected_book = st.selectbox("Did you mean?", matched_books) if matched_books.size > 0 else ""
    
    if selected_book:
        recommendations = recommend(selected_book, data, similarity, merge_df1)
    else:
        recommendations = []

    if recommendations:
        def display_recommendations(recommendations):
            """Display book recommendations with clickable titles."""
            num_books = len(recommendations)
            cols = st.columns(num_books)

            for col, book in zip(cols, recommendations):
                with col:
                    image_url = book.get("Image-URL-L", "https://via.placeholder.com/150")
                    st.image(image_url, use_column_width=True)

                    if st.button(f"📖 {book['Book-Title'].title()}"):
                        st.session_state.selected_book = book['Book-Title']
                        st.rerun()

                    # Wrap book details inside a black box
                    st.markdown(
                        f"""
                        <div class="book-details">
                            ✍️ <b>Author:</b> {book['Book-Author']} <br>
                            📅 <b>Year:</b> {book['Year-Of-Publication']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        
        display_recommendations(recommendations)
    else:
        st.warning("❌ No recommendations found. Try another book.")
