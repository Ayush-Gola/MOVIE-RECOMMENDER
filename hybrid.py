import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np

movies_dict_con = pickle.load(open('movies_cont.pkl','rb'))
movies_con = pd.DataFrame(movies_dict_con)
similarity_con = pickle.load((open('similarity_cont.pkl','rb')))

similarity_col = pickle.load(open('similarity_col.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))

def fetch_poster_con(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{0}?api_key=be6df6e555f848fba7f61656104ff43e&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend_con(movie):
    movie_index = movies_con[movies_con['title'] == movie].index[0]
    ditances = similarity_con[movie_index]
    movies_list = sorted(list(enumerate(ditances)),reverse=True,key=lambda x:x[1])[1:11]
    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies_con.iloc[i[0]].movie_id
        recommend_movies.append(movies_con.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster_con(movie_id))
    return recommend_movies,recommend_movies_posters


def id(name):
    tmdbId = movies_con[movies_con['title'] == name].movie_id.values[0]
    return tmdbId

def fetch_poster_col(tmdbId):
    response = requests.get('https://api.themoviedb.org/3/movie/{0}?api_key=be6df6e555f848fba7f61656104ff43e&language=en-US'.format(tmdbId))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend_col(name):
    tmdbId = movies_con[movies_con['title'] == name].movie_id.values[0]
    index = np.where(pt.index == tmdbId)[0][0]
    similar_movies = sorted(list(enumerate(similarity_col[index])),key=lambda x:x[1],reverse=True)[1:11]
    movies_list = []
    poster_list = []
    for i in similar_movies:
        movies_list.append(movies_con[movies_con['movie_id'] == pt.index[i[0]]].title.values[0])
        x = id(movies_con[movies_con['movie_id'] == pt.index[i[0]]].title.values[0])
        y = fetch_poster_col(x)
        poster_list.append(y)
    return movies_list,poster_list

st.set_page_config(layout="wide")

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.pexels.com/photos/3379934/pexels-photo-3379934.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
add_bg_from_url() 

st.title('_Movies Recommender System_')
selected = st.selectbox('Select any one movie for Recommendations:',movies_con['title'].values)
names = []
posters = []
if st.button('Recommend Movies'):
    names1,posters1 = recommend_con(selected)
    names2,posters2 = recommend_col(selected)
    for i in range(len(names1)):
        names.append(names1[i])
        names.append(names2[i])
        posters.append(posters1[i])
        posters.append(posters2[i])
    names = [i for n, i in enumerate(names) if i not in names[:n]]
    posters = [i for n, i in enumerate(posters) if i not in posters[:n]]
    st.header('We recommend you these movies on basis of your choice:')
    for i in range(2):
        col1, col2,col3,col4,col5 = st.columns(5)
        with col1:
            st.subheader(names[0 + 5*i])
            if posters[0 + 5*i]:
                st.image(posters[0 + 5*i],use_column_width='auto')
        with col2:
            st.subheader(names[1 + 5*i])
            if posters[1 + 5*i]:
                st.image(posters[1 + 5*i],use_column_width='auto')
        with col3:
            st.subheader(names[2 + 5*i])
            if posters[2 + 5*i]:
                st.image(posters[2 + 5*i],use_column_width='auto')
        with col4:
            st.subheader(names[3 + 5*i])
            if posters[3 + 5*i]:
                st.image(posters[3 + 5*i],use_column_width='auto')
        with col5:
            st.subheader(names[4 + 5*i])
            if posters[4 + 5*i]:
                st.image(posters[4 + 5*i],use_column_width='auto')
        