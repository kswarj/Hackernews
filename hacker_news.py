# import requests and json modules
import requests
import json

#import pandas 
import pandas as pd
from pandas import json_normalize

#import asyncio and aiohttp
import asyncio
import aiohttp

#import flask and render template
from flask import Flask, render_template

max_url_stories = 50

#get hackernews top stories with max length limited to 500
def get_topstories():

    #Hackernews url for newstories
    base_url = f'https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty'

    #send get request for Hackernews restAPI
    r = requests.get(base_url)

    #check for status code
    if  (r.status_code) != 200:
        raise ValueError(f'top stories status code:{r.status_code}')
    
    # assigning the items in a list
    global top_stories 
    top_stories = r.json()

    #return list of item ids
    return top_stories

#asynchronous function to process url in batches and upto a length of 500, size of hackernews item max length
async def process_urls(urls, batch_size):

    #create a aiohttp client session  for makingayncronous http requests
    async with aiohttp.ClientSession() as session:
        batches = [urls[i:i+batch_size] for i in range(0, len(urls), batch_size)]
        results = []
        for batch in batches:
            batch_results = await process_batch(session,batch)
            results.extend(batch_results)
        return results

#asynchronous function to process  each url as task and append to tasks list
async def process_batch(session,urls):
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(fetch_data(session,url))
        tasks.append(task)
    return await asyncio.gather(*tasks)
    

async def main():
    
    #define base url string  to capture each item id returned from the list in top_stories
    url_item = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty"
    
    #get all the url string in a list
    urls = [url_item.format(item) for item in top_stories]
    
    #process each url in a list with process url function
    results = await process_urls(urls, max_url_stories)

    #capture the results in json results in a dataframe
    df = pd.json_normalize(results)
    df.set_index('id', inplace=True)
    return(df)


#asynchronous function to fetch data from given url using aiohttp
async def fetch_data(s,u):
    #use session.get() to make a  asynchronous http request
    async with s.get(u) as response:
        return await response.json()


#Define app flask application route to display on browser
app = Flask(__name__)
@app.route("/tables")
def show_tables():
    return(render_template('index.html', table=table.to_html(classes='table table-stripped')))
   

if __name__ == '__main__':
    # get the top story list from hackernew website
    get_topstories()

    #get the table from the dataframe sorted  with id from the main function
    table = asyncio.run(main())

    #use localhost routing with flask app to the webbrowser
    app.run(debug=True)
