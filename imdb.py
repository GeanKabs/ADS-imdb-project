#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 19:41:45 2022

@author: gk
"""

import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title='IMDb Movie Ratings Dashboard')

#Loading the available data and overview
path = "movies_8100.csv"
st.sidebar.header('Top 8100 Movies')
data = st.sidebar.file_uploader("Upload Dataset", type=['csv', 'txt', 'xlsx'])

#Checking for uploaded dataset
if data is not None:
    df = pd.read_csv(data, encoding="ISO-8859-1", low_memory=False).dropna()
    df["release year"] = pd.Datetime(df["release date"]).year
    # df["Movie_Title"] = df["movie title"]
    
    
#Default Dataset if none is uploaded    
else:
    df = pd.read_csv(path, encoding="ISO-8859-1", low_memory=False)
    df["release date"] = df["release date"]
    df["release year"] = pd.DatetimeIndex(df["release date"]).year
    #df["roundOff release"] = df["cumulative worldwide"].round(-9)
    # df["Movie_Title"] = df["movie title"]

#Adding select boxes for different comaands and functionalities
menu = ['IMDb Movies Snapshot', 'Analysis', 'About']
selection = st.sidebar.selectbox("Key Performance Indicator (KPI) ", menu)

st.sidebar.write(''' Building a Regression model to predict the IMDb rating of a movie using features that are only available prior to its release.''')

if selection == 'IMDb Movies Snapshot':
    st.subheader('Display data')
    st.dataframe(df.head(10))
 
    
    col1, col2 = st.columns(2)
    # Column 1
    with col1:
        #Budget
        st.subheader("Budget")
        df_budget = df["release year"]
        plt.figure(figsize=(20,15))
        sns.barplot(x="release year", y="budget",  data=df.head(40))
        #sns.barplot(x="release year", y="budget", hue="movie title", data=df.head(40))
        plt.title("Budget")
        plt.xlabel("Year")
        plt.ylabel("Budget")
        st.pyplot(plt)
    # Column 2
    with col2:
        # cumulative worldwide returns
        st.subheader("Cumulative Wordwide Returns")
        df_AvgRuntime = df.groupby(["runtime (min)"]).count().reset_index()
        df_cumulativeWordwide = df["cumulative worldwide"]
        plt.figure(figsize=(15,10))
        sns.barplot(x="cumulative worldwide", y="runtime (min)", data=df.head(40))
        #sns.barplot(x="runtime (min)", y="cumulative worldwide", hue="movie title", data=df.head(40))
        plt.title("Cumulative worldwide returns")
        plt.xlabel("cumulative worldwide($)")
        #plt.xlabel("runtime(min)")
        plt.ylabel("runtime (min)")
        #plt.ylabel("cumulative worlwide($)")
        st.pyplot(plt)
        
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Pairplot Visualisation ")
        # Pairplot visualisation
        df_moviesDropB = df.dropna(subset=['budget']) #Dropping movies without budget data
        sns.pairplot(df_moviesDropB, height=1.2, aspect=1.25)
        st.pyplot(plt)
    with col4:
        st.subheader("imdb rating Vs writer")
        plt.figure(figsize=(15,10))
        sns.barplot(x="writer", y="imdb rating", data=df.head(7))
        plt.title("IMDb Ratings - Writers")
        plt.xlabel("Wirter")
        plt.ylabel("IMDb Ratings")
        st.pyplot(plt)
        
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Best Movies by Genre Revenue")
        df["Revenue"] = df["cumulative worldwide"]
        df_bestRevenue = df.groupby('genres').Revenue.sum().reset_index()
        df_bestRevenue.columns = ['genres', 'Revenue']
        df_bestRevenue.sort_values(by='Revenue', inplace=True, ascending=False)
        df_bestRevenue.reset_index(inplace=True, drop=True)
        top_5_sales = df_bestRevenue.iloc[:5]
        plt.figure(figsize=(15,10))
        plt.pie(top_5_sales['Revenue'],
                labels=top_5_sales['genres'],
                wedgeprops={'edgecolor': 'black'},
                startangle=90,
                radius=1.1,
                counterclock=False,
                autopct='%1.1f%%'
                )
        plt.title('Best performing Genres')
        st.pyplot(plt)
        
    with col6:
        st.subheader("Worst Movies by Genre (Revenue)")
        bottom_5_sales = df_bestRevenue.iloc[5:]
        plt.figure(figsize=(15,10))
        plt.pie(bottom_5_sales['Revenue'],
                labels=bottom_5_sales['genres'],
                wedgeprops={'edgecolor': 'black'},
                startangle=90,
                radius=1.1,
                counterclock=False,
                autopct='%1.1f%%',
                )
        plt.title('Worst Performing Genres')
        st.pyplot(plt)
        
    # New Movies Vs. Older Movies
    st.header("New Movies Vs. Older Movies")
    df_newMovies = df.groupby(["movie title"])['release year'].min().reset_index()
    df_newMovies.columns = ["movie title", "release date"] 
    df2 = pd.merge(df, df_newMovies, on="movie title")
    df2["NewMovie"] = "New"
    df2.loc[df2["release year"] > df2["release year"], "NewMovie"]
    
    df2.head()
    # New Vs. Existing User Revenue Analysis
    df_newMoviesRevenue = df2.groupby(["release year", "NewMovie"])["Revenue"].sum().reset_index()
    plt.figure(figsize=(30, 20))
    sns.relplot(x="release year", y="Revenue", hue="NewMovie", data=df_newMoviesRevenue, kind="line", height=12,
                aspect=18 / 10 )
    plt.title("New Vs Older Movies Revenue Overview")
    plt.xlabel("release date")
    plt.ylabel("Revenue")
    st.pyplot(plt)
    
elif selection == 'Analysis':
    st.subheader('Display data')
    st.write(df.head(5))
    #Shape of data
    if st.checkbox("show shape "):
        st.write('Data Shape ')
        st.write('{:,} rows; {:,} columns'.format(df.shape[0], df.shape[1]))
        
        #data descriptiion
        st.markdown("Description statistics ")
        st.write(df.describe())
       
# adding html Template
footer_temp = """
<!-- CSS -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
type="text/css" rel="stylesheet" media="screen,projection"/>
<link href="static/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzIco0wtJAoU8YZTY5qE01d1GSseTk6S+L3BlxeVIU" crossorigin="anonymous">
footer class="page-footer grey darken-4">
<div class ="container" id="aboutapp">
<div class="row">
<div class="col 16 s12">
<h5 class="white-text">Movie Analysis App</h5>
<h6 class="grey-text text-lighten-4">This is Africa Data School</p>
<p class="grey-text text-lighten-4">January 2022 Cohort</p>
</div>
<div class="col l3 s12">
<h5 class="white-text">Connect with Us</h5>
<ul>
<a href="https://www.facebook.com/AfricaDataSchool/" target="_blank" class="white-text">
<i class="fab fa-facebook fa-4x"></i>
</a>
<a href="https://www.linkedin.com/company/africa-data-school" target="_blank" class="white-text">
<i class="fab fa-linkedin fa-4x"></i>
</a>
<a href="https://www.youtubr.com/watch?v=zRdlQwNTJo" target="_blank" class="white-text">
<i class="fab fa-youtube-square fa-4x"></i>
</a>
<a href="https://github.com/Africa-Data-School" target="_blank" class="white-text">
<i class="fab fa-github-square fa-4x"></i>
</a>
</ul>
</div>
</div>
</div>
<div class="footer-copyright">
<div class="container">
Made by <a class="white-text text-lighten-3" href="https://africadataschool.com/">Re.... </a><br/>
<a class="white-text text-lighten-3" href="https://africadataschool.com"></a>
</div>
</div>
</footer>
"""

if selection == 'About':
    st.header("About App")
    components.html(footer_temp, height=500)
    


    
    

        
                 
        
    
    
