
![image](https://github.com/user-attachments/assets/aa6033b6-10ef-4701-869c-4d21016d7cb9)

# 📚 Book Recommendation System

## Overview
This Book Recommendation System suggests books based on user input. It uses a **popularity-based recommendation approach**, meaning it recommends books that are widely liked and rated highly by users. The system also allows users to refine recommendations by selecting any recommended book to get further suggestions.

## Approach
We built this system using a **popularity-based filtering method**, where books are recommended based on:
1. **Number of Ratings:** Books with more ratings are prioritized.
2. **Average Rating:** Higher-rated books are given preference.
3. **User Engagement:** Books frequently interacted with by users are considered.
4. **Similarity Metrics:** A similarity matrix (based on book features and user preferences) is used to enhance recommendations.

The system leverages the **Book-Crossing dataset**, which includes book details, user reviews, and ratings to generate the most relevant suggestions.

## Dataset
The dataset used for this project is the **Book-Crossing dataset**, sourced from **Kaggle**. It consists of three main tables:
1. **Books Dataset:** Contains information about books.
   - `ISBN`: Unique identifier for books.
   - `Book-Title`: Title of the book.
   - `Book-Author`: Author of the book.
   - `Year-Of-Publication`: Year the book was published.
   - `Publisher`: Name of the publisher.
   - `Image-URL-S`, `Image-URL-M`, `Image-URL-L`: URLs of book cover images (small, medium, and large).

2. **Users Dataset:** Contains user information.
   - `User-ID`: Unique user identifier.
   - `Location`: User's location.
   - `Age`: Age of the user (if available).

3. **Ratings Dataset:** Contains book ratings given by users.
   - `User-ID`: ID of the user who rated the book.
   - `ISBN`: The book that was rated.
   - `Book-Rating`: Rating given by the user (0-10 scale).

After preprocessing, the dataset contains **900 users** and **690 books**.

## Features
- 📖 **Search Books:** Find books by entering partial or full titles.
- 🔥 **Top 5 Recommendations:** Get five similar books based on the selected book.
- 🔄 **Interactive Recommendations:** Click on a recommended book to get further suggestions.
- 🎨 **Beautiful UI:** A visually appealing interface with a background image and side-by-side book recommendations.

## Tech Stack
- **Python** (for backend processing)
- **Streamlit** (for UI)
- **Pandas & NumPy** (for data processing)
- **Pickle** (to store precomputed similarity matrix)

## Installation

Hosted App
🚀 Try out the live demo: Book Recommender System

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/book-recommender.git
   cd book-recommender
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Enter a book title or a keyword.
2. Select the book from suggestions (if multiple matches are found).
3. View the top 5 recommended books.
4. Click on any recommended book to get further recommendations.

## Screenshots
![image](https://github.com/user-attachments/assets/71c8cc1e-dc02-4631-9e2d-b8500d8fec2d)

## Future Improvements
- 📌 **Hybrid Recommendation System** (combining content-based & collaborative filtering)
- 🚀 **Deployment on Streamlit Cloud / Heroku**
- 📊 **User-Based Personalization**

## Contributing
Feel free to fork, improve, and submit pull requests. Contributions are welcome! 😊

## License
This project is open-source and available under the **MIT License**.


