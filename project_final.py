# # Libraries to be installed

# !pip install pandas
# !pip install requests
# !pip install bs4
# !pip install plotly
# !pip install geopy


from flask import Flask, render_template, request
import requests
import pandas as pd
import numpy as np
import json
import geopy
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe


from codes import code_g
from codes import code_b
from codes import code_f
from codes import code_clean

app = Flask(__name__)


search_item =" "


total_searches=[]

## Creating a class search 

class search:
    count_search=-1
    def __init__(self,search_food,search_location,search_city):
        self.search_food=search_food
        self.search_location=search_location
        self.search_city=search_city

        search.count_search +=1

        self.data_google= code_g.search_google(search_food,search_location,search_city)
        self.data_bing= code_b.search_bing(search_food,search_location,search_city)
        self.data_4s= code_f.search_4s(search_food,search_location,search_city)

        self.data_df= code_clean.cleaning(self.data_google,self.data_bing,self.search_location)
        self.data=self.data_df.to_dict()
        


@app.route('/')
def index():
    return render_template('main.html')



@app.route('/submitform/', methods=['post'])
def submitform():
    result = request.form

    submitform.foodtype= result["food_type"]
    submitform.location = result["location"]
    submitform.city=result["city"]

    total_searches.append(search(submitform.foodtype,submitform.location,submitform.city))

    search_item = submitform.foodtype + ' ' + submitform.location + ' ' + submitform.city
    print(search_item)
    print(total_searches[search.count_search].data_df)
    data=total_searches[search.count_search].data
    print(data)
    print('Total searches done till now', search.count_search+1)

    data_r=total_searches[search.count_search].data_4s

    return render_template('search.html', b=data, c=data_r)



@app.route('/submitform1/', methods=['post'])
def submitform1():
    result1 = request.form
    foodtype1= result1["search"]

    total_searches.append(search(foodtype1,submitform.location,submitform.city))

    print(total_searches[search.count_search].data_df)
    data=total_searches[search.count_search].data
    print(data)
    print('Total searches done till now', search.count_search+1)

    data_r=total_searches[search.count_search].data_4s
   
    return render_template('search.html', b=data, c=data_r)


if __name__ == '__main__':
    app.run()