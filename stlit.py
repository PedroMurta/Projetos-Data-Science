import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


st.title('Recomendation IMDB Series :blue_book:')
st.image('imdb.jpg', width=500)


#@st.cache(allow_output_mutation=True)
def get_data():
    return pd.read_csv('series_data.xls')

df = get_data()

df.columns = ['Poster', 'Title', 'RuntimeSeries', 'Certificate', 'RuntimeEpisode', 'Genre', 'Rating', 'Overview', 'Actor1', 'Actor2', 'Actor3', 'Actor4', 'NVotes']


def categoriza(s):
    if s == '16+':
        return '16'
    elif s == '18+':
        return '18'
    elif s == 'U':
        return '0'
    elif s == '7+':
        return '7'
    elif s == '15+':
        return '15'
    elif s == '12+':
        return '12'
    elif s == 'All':
        return '0'
    elif s == '13+':
        return '13'
    elif s == 'A':
        return '18'
    elif s == 'Not Rated':
        return '13'
    elif s == 'R':
        return '17'
    elif s == 'UA':
        return '12'
    elif s == 'PG':
        return '12'
    elif s == '18':
        return '18'
    elif s == '15':
        return '15'


df['Certificates'] = df['Certificate'].apply(categoriza)
df['RuntimeEpisodes'] = df.RuntimeEpisode.astype(str).str.replace(' min', '')



df.Certificates.fillna(df['Certificates'].mode(), inplace=True)
df.RuntimeEpisodes.fillna(df['RuntimeEpisodes'].mode(), inplace=True)


df.drop('Certificate', axis=1, inplace=True)
df.drop('RuntimeEpisode', axis=1, inplace=True)


from sklearn.feature_extraction.text import TfidfVectorizer
cv = TfidfVectorizer(stop_words='english')
cvm = cv.fit_transform(df['Overview'].values.astype('U'))


from sklearn.metrics.pairwise import linear_kernel
s = linear_kernel(cvm, cvm)
indices = pd.Series(df.index, index=df.Title).drop_duplicates() 


def getRecomendations(title, s=s):
    idx = indices[title]
    # Spairwise similarity scores of all series with that serie
    s_scores = list(enumerate(s[idx]))
    # Sortr series based on similarity scores
    s_scores = sorted(s_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of 10 most similar series
    s_scores = s_scores[1:6]
    # get the indices series
    #serie_indices = [i[0] for i in s_scores]
    serie_indices = [i[0] for i in s_scores]
    # Return the top 10 similar
    return df['Title'].iloc[serie_indices]

@st.cache(allow_output_mutation=True)

def buttons(i):
    for i in range(df['Title']):
        if i == True:
            return getRecomendations(df.Title[i])
        else:
            return 'Algo Não funcionou'''


st.sidebar.image("image2.jpg", width=300)
value = st.sidebar.selectbox('Select one TV Show', df['Title'])


st.markdown('## *You may also Like * :sunglasses:')
st.write('Based on your history ', getRecomendations(value))

st.write('*Title Selected:* ', value)



st.sidebar.write('') 
st.sidebar.write(' *Made With* :heart:')
st.sidebar.write('*Pedro Murta Lima*')
st.sidebar.write('*Analista de Sistemas e Pós-Graduando em Ciência de Dados*')
st.sidebar.write('*PUC-Minas*')