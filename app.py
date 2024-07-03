import requests
import streamlit as st
import pickle
import pandas as pd

# CSS for custom styling
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #b7410e; /* light rust color */
    }
    .movie-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
    }
    .movie-title {
        font-size: 14px; /* Smaller font size */
        color: white; /* Font color for better contrast */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=5d8e0a103fc508014279e1f9f103119d&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_images = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_images.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_images

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender')
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

if st.button('Search'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{poster}" alt="{name}" style="width:100%;border-radius:10px;">
                    <div class="movie-title">{name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
