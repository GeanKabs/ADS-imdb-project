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
path = "/home/gk/Projects Exercises/imdb/movies_8100.csv"
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
        '''
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
        '''
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
        
        
        
                 
        
    
    
