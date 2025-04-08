import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import time
import os

@st.cache_data  
def load_data():
    csv_filename = "news_data.csv"
    if os.path.isfile(csv_filename):
        df = pd.read_csv(csv_filename)
        df['published'] = pd.to_datetime(df['published'])
        return df
    else:
        return pd.DataFrame()  

df = load_data()

# extraire date court
df['published'] = df['published'].astype(str).str[:22]
df['published'] = pd.to_datetime(df['published'])

st.title("📊 Dashboard France TV Info")

# Filtre par catégorie
st.sidebar.header("Filtres")
categories = df['categorie'].unique().tolist()
selected_categories = st.sidebar.multiselect("Sélectionnez les catégories", categories, default=categories)

if selected_categories:
    df = df[df['categorie'].isin(selected_categories)]

# Filtre par date
min_date = df['published'].min().to_pydatetime() 
max_date = df['published'].max().to_pydatetime() 
start_date, end_date = st.sidebar.slider(
    "Sélectionnez la plage de dates",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

if start_date and end_date:
    df = df[(df['published'] >= start_date) & (df['published'] <= end_date)]

# cartes
col1, col2, col3, col4 = st.columns(4)
col4.metric("Total société 🏢", df[df['categorie'] == 'societe'].shape[0])
col2.metric("Total science 🔬", df[df['categorie'] == 'science'].shape[0])
col3.metric("Total économie 💰", df[df['categorie'] == 'economie'].shape[0])
col1.metric("Total data 📊", df.shape[0])

# Pie chart
st.header("🛞 Répartition des données par catégorie")
fig_pie = px.pie(df, names='categorie')
st.plotly_chart(fig_pie)

# Line plot
st.header("🚀 Évolution du nombre de données collectées")
df_daily_count = df.groupby(df['published'].dt.date)['title'].count().reset_index()
fig_line = px.line(df_daily_count, x='published', y='title')
st.plotly_chart(fig_line)

#df
st.header("Données")
st.dataframe(df)
