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

# # using google search
apikey_google = "AIzaSyCOdjxISTnv9a1IhxSz0VQo1B0LDe1xw-0"
engineid_google = "9aade3108823ded77"

def search_google(food,locat,cit):
    
    search_item = food + ' ' + locat + ' ' + cit 
    print(search_item)
    url_google = f"https://www.googleapis.com/customsearch/v1?key={apikey_google}&cx={engineid_google}&q={search_item}"

    result_google = requests.get(url_google).json()

    df_google=pd.DataFrame(columns=['Name','url','description','image'])
    dmg = result_google['items']
    # dmg
    i=0
    while i <10:
        print(i)
        if 'cse_image' in dmg[i]["pagemap"]:
            i=i
            print('new',i)
            n= dmg[i]['title']
            url=dmg[i]['link']
            d= dmg[i]['snippet']
            image=dmg[i]["pagemap"]['cse_image'][0]['src']
            print(i)
            df_google = df_google.append({'Name':n,'url':url,'description':d,'image':image}, ignore_index=True)
        i=i+1
    return(df_google)
   

