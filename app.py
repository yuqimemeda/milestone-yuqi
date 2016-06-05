from flask import Flask, render_template, request, redirect, url_for
from pandas import DataFrame, to_datetime
import pandas
import numpy as np
import json
import requests
import time
from datetime import datetime,timedelta
from bokeh.plotting import figure, output_file, show
from bokeh import embed
import cgi
from bokeh.embed import components 

#build the app
app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
    return render_template('index.html')


def plotting():
    
    
    #user's input
    ticker = request.form['ticker']
    #calculate the time one month before
    now = datetime.now()
    #calculate the time difference
    start_date = (now - timedelta(days=30)).strftime('%Y-%m-%d')
    #fetch the dataset
    URL = 'https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?start_date='+start_date+'&order=asc&api_key=WVEFZw8uyJzuvHE3VsQW'
    r = requests.get(URL)
    
    
    #pass to pandas dataframe
    raw_data = DataFrame(r.json())
    #clean up the data
    df = DataFrame(raw_data.ix['data','dataset'] , columns = raw_data.ix['column_names','dataset'])
    
    
    #convert the index to datetime 
    df['Date'] = to_datetime(df['Date'])
    
    #create the plot
    p = figure(x_axis_type = "datetime")
    
    p.line(df['Date'], df['Close'], color='green', legend='closing price')
    return p

@app.route('/chart_page',methods=['GET','POST'])
def chart():
    plot = plotting()
    script, div = embed.components(plot)
    return render_template('bokeh.html', script=script, div=div)


    
if __name__ == '__main__':
    
    app.run(port=33507,debug=True)

    
