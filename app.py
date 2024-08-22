# import requests and json modules
import requests
import json

#import pandas 
import pandas as pd
from pandas import json_normalize

#import flask and render template
from flask import Flask, render_template



def get_url_hackernews():
    #Hackernews url for newstories
    base_url = f'https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty'

    #send get request for Hackernews restAPI
    r = requests.get(base_url)

    #store response data in value
    value = (r.json())

    #Calulate top 10 new stories
    l = value[0:10]
    
    #Initlialize a list for appending a dict of values for each news item
    new_dict=[]

    #for lopp to iterate through each item of new
    for item in l:
        
        #get each item url with item id
        item_url = f'https://hacker-news.firebaseio.com/v0/item/{item}.json?print=pretty'
        
        #send Rest API get request
        new = requests.get(item_url)

        #store the dict keys and values from json in a variable
        latest_news = new.json()

        #append the dict of items in a list
        new_dict.append(latest_news)
    
    #create a Dataframe and normalize the Json data 
    df = pd.json_normalize(new_dict)

    #set the Dataframe index based on the news item id
    df.set_index('id',inplace=True)
    # return the dataframe
    return(df)

#Define app flask application route to display on browser
app = Flask(__name__)
@app.route("/tables")
def show_tables():
    return(render_template('index.html', table=table.to_html(classes='table table-stripped')))
 

if __name__ =='__main__':
    table =  get_url_hackernews()
    #print the table
    #print(table)
    app.run(debug = True)


