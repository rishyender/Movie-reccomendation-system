import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = "c82039a88c9816b639558243313cc2e2"

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

        response = requests.get(url)

        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

        return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception as e:
        print(e)
        return "https://via.placeholder.com/300x450?text=Error"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

st.title('MOVIE RECOMMENDER SYSTEM')

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

selected_movie_name= st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
#fro running streamlit run.app.py
