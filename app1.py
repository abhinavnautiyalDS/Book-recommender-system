import streamlit as st
import pickle
import pandas as pd
import numpy as np
import gdown
import base64
import os

# Install dependencies from requirements.txt
if not os.path.exists(".installed_dependencies"):  # Run only once
    os.system("pip install -r requirements.txt")
    open(".installed_dependencies", "w").close()

# Google Drive file ID
file_id = "191k7cqEm0JZmhdBujowlT9CroGTrWZ1c"
output_file = "recommend.pkl"

gdown.download(f"https://drive.google.com/uc?id={file_id}", output_file, quiet=False)

# Load the recommendation function and data
with open(output_file, "rb") as file:
    data_dict = pickle.load(file)

data = data_dict["data"]
similarity = data_dict["similarity"]
merge_df1 = data_dict["merge_df1"]

def search_books(query, merge_df1):
    query = query.strip().lower()
    merge_df1["Book-Title"] = merge_df1["Book-Title"].str.strip().str.lower()
    results = merge_df1[merge_df1["Book-Title"].str.contains(query, na=False)]["Book-Title"].unique()
    return results[:5]

def recommend(book_name, data, similarity, merge_df1):
    book_name = book_name.strip().lower()
    data.index = data.index.str.strip().str.lower()
    
    if book_name not in data.index:
        st.warning(f"❌ '{book_name}' not found in dataset.")
        return []
    
    index = np.where(data.index == book_name)[0][0]
    similar_indices = np.argsort(-similarity[index])[1:6]
    book_titles = data.iloc[similar_indices].index.tolist()
    
    merge_df1["Book-Title"] = merge_df1["Book-Title"].str.strip().str.lower()
    book_titles = [title.lower() for title in book_titles]
    
    info = merge_df1[merge_df1["Book-Title"].isin(book_titles)][
        ["Book-Title", "Book-Author", "Year-Of-Publication", "ISBN", "Image-URL-L"]
    ].drop_duplicates(subset="Book-Title", keep="first")
    
    return info.to_dict(orient="records")

st.set_page_config(layout="wide")

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error("Image file not found!")
        return None

image_base64 = get_base64_image("image (79).png")

if image_base64:
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
    st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 60px;'>📚 Book Recommendation System</h1>", unsafe_allow_html=True)

query = st.text_input("📖 Enter a book title or keyword:")

if query:
    matched_books = search_books(query, merge_df1)
    selected_book = st.selectbox("Did you mean?", matched_books) if len(matched_books) > 0 else ""
    recommendations = recommend(selected_book, data, similarity, merge_df1) if selected_book else []
    
    if recommendations:
        cols = st.columns(len(recommendations))
        for col, book in zip(cols, recommendations):
            with col:
                st.image(book.get("Image-URL-L", "https://via.placeholder.com/150"), use_column_width=True)
                st.markdown(f"**{book['Book-Title'].title()}**")
                st.markdown(f"✍️ **Author:** {book['Book-Author']}  ")
                st.markdown(f"📅 **Year:** {book['Year-Of-Publication']}")
    else:
        st.warning("❌ No recommendations found. Try another book.")
