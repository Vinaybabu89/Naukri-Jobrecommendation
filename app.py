# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 16:40:58 2021

@author: vinay
"""

import pandas as pd
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
# libraries for making count matrix and similarity matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def create_sim():
    data = pd.read_csv('Recom1.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['text'])
    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return data,sim

def rcmd(m):
    #m = m.lower()
    # check if data and sim are already assigned
    try:
        data.head()
        sim.shape
    except:
        data, sim = create_sim()
    # check if the movie is in our database or not
    if m not in data['Job_Roles'].unique():
        return('This job_roles is not in our database.\nPlease check if you spelled it correct.')
    else:
        # getting the index of the movie in the dataframe
        i = data.loc[data['Job_Roles']==m].index[0]

        # fetching the row containing similarity scores of the movie
        # from similarity matrix and enumerate it
        lst = list(enumerate(sim[i]))

        # sorting this list in decreasing order based on the similarity score
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)

        # taking top 1- movie scores
        # not taking the first index since it is the same movie
        lst = lst[1:11]

        # making an empty list that will containg all 10 movie recommendations
        l = []
       
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['Details'][a])
            
            
                        
       
        return l
  
    
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

#@app.route("/basic")
#def home():
    #return render_template('home.html')

@app.route("/recommend")
def recommend():
    Job_Roles = request.args.get('Job_Roles')
    r = rcmd(Job_Roles)
    #movie = movie.upper()
    if type(r)==type('string'):
        return render_template('recommend.html',Job_Roles=Job_Roles,r=r,t='s')
    else:
        return render_template('recommend.html',Job_Roles=Job_Roles,r=r,t='l')
        #return render_template('jobs.html',Job_Roles=Job_Roles,r=r,t='text_file')
        



if __name__ == '__main__':
    app.run()
