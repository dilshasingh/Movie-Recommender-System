import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    return ""

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")

# Create a dropdown to select a movie from the list
selected_movie = st.selectbox("Select a movie:", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

if st.button("Show Recommend"):
    movie_names, movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for col, movie_name, movie_poster in zip(cols, movie_names, movie_posters):
        with col:
            st.text(movie_name)
            if movie_poster:
                st.image(movie_poster)
            else:
                st.text("No image available")
